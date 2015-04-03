import os
import subprocess
import tempfile
from datetime import datetime, date

from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils.timezone import now

import yaml
from docusearch.models import Document, ImportLog


def is_date(d):
    """ If 'd' is all digits, return True as in our system this signifies it
    represents a date. """
    return d.isdigit()


def text_to_date(date_string):
    """ Given a string that represents a date in YMD format, return an
    equivalent Date object. """

    return datetime.strptime(str(date_string), '%Y%m%d').date()


def copy_and_extract_documents(agency_directory, d):
    """ Extract text from documents, and return a tuple contain documentation
    details and the extracted text. """

    date_dir = os.path.join(agency_directory, d)
    manifest_path = os.path.join(date_dir, 'manifest.yaml')
    manifest = yaml.load(open(manifest_path, 'r'))

    for document in manifest:

        doc_path = os.path.join(date_dir, document['doc_location'])
        root, ext = os.path.splitext(doc_path)
        text_doc_path = root + '.txt'
        # Check if the text file actually exists
        if os.path.exists(text_doc_path):
            text_contents = open(root + '.txt', 'r').read()
            if len(text_contents) > 5000:
                text_contents = text_contents[:5000]
            yield(document, doc_path, text_contents)
        else:
            yield None


def convert_to_text(file_name, doc_path):
    """ Given a pdf, extract the text. We will later be a bit more
    sophisticated here. """

    file_name_base = file_name.split('.')[0]
    extracted_folder = tempfile.gettempdir()

    right_now = now().strftime("%Y%m%d%H%M%S")
    extracted_file = os.path.join(
        extracted_folder, '%s%s.txt' % (file_name_base, right_now))
    subprocess.check_call(['pdftotext', doc_path, extracted_file], shell=False)
    return extracted_file


def create_basic_document(document, release_slug):
    """ Create a basic Document object (without the file upload related bits)
    """

    details, _, text_contents = document
    d = Document()
    d.text = text_contents

    title = details.get('title')
    if title:
        d.title = title

    date_created = details.get('date_created')
    if date_created:
        d.date_created = date_created

    pages = details.get('pages')
    if pages and pages != "null":
        d.pages = pages

    date_released = details.get('date_released')
    if date_released:
        d.date_released = date_released

    d.release_agency_slug = release_slug

    file_type = details.get('file_type')

    # Only save pdfs for now
    if file_type == 'pdf':
        d.file_type = file_type
        return d


def create_document(document, release_slug):
    """ Create a Document object representing the document. This also uploads
    the document into it's S3 location. """

    d = create_basic_document(document, release_slug)
    details, doc_path, text_contents = document

    doc_file = File(open(doc_path, 'rb'))
    filename = os.path.basename(doc_path)

    # On save() django-storages uploads this file to S3
    if d:
        d.original_file.save(filename, doc_file, save=True)


def unprocessed_directory(date_directory, agency, office=None):
    """ If we've completely processed a directory of documents, we will have an
    ImportLog entry for it. Return False if this is the case. """

    existing_logs_count = ImportLog.objects.filter(
        agency_slug=agency,
        office_slug=office,
        directory=date_directory).count()
    return existing_logs_count == 0


def mark_directory_processed(date_directory, agency, office=None):
    """ This simply creates an ImportLog entry, marking date_directory as
    having been processed for this agency/office combination. """

    il = ImportLog(
        agency_slug=agency,
        office_slug=office,
        directory=date_directory,
    )
    il.save()


def import_log_decorator(date_directory, agency, office, process_documents):
    if unprocessed_directory(date_directory, agency, office):
        process_documents()
        mark_directory_processed(date_directory, agency, office)


def process_date_documents(
        date_directory, parent_directory, agency, office=None):
    release_slug = agency
    if office:
        release_slug = '%s-%s' % (agency, office)

    def process():
        for document in copy_and_extract_documents(
                parent_directory, date_directory):
            # Only import documents that have text file
            if document:
                create_document(document, release_slug)

    import_log_decorator(date_directory, agency, office, process)


def process_office(agency_directory, agency, office_name):
    """ Process an Office directory, which will contain several sub-directories
    that are named after dates (which contain the actual documents. """

    office_directory = os.path.join(agency_directory, office_name)
    for date_directory in os.listdir(office_directory):
        process_date_documents(
            date_directory, office_directory, agency, office_name)


def process_agency(documents_directory, agency):
    """ An Agency directory can either have sub-Office directories, or date
    named directories that contain actual documents. This processes both
    appropriately. """

    agency_directory = os.path.join(documents_directory, agency)

    for d in os.listdir(agency_directory):
        if is_date(d):
            process_date_documents(d, agency_directory, agency)
        else:
            process_office(agency_directory, agency, d)


class Command(BaseCommand):
    help = "Import documents from your document source, into docusearch."

    def handle(self, *args, **options):
        if len(args) > 0:
            documents_directory = args[0]
            agencies = os.listdir(documents_directory)
            for agency in agencies:
                process_agency(documents_directory, agency)
        else:
            print('python manage.py import_documents <<document/import/path>>')
