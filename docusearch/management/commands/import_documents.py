import os
import shutil
import subprocess
from datetime import datetime
from django.core.management.base import BaseCommand
import yaml

from docusearch.models import Document


def is_date(d):
    """ If 'd' is all digits, return True as in our system this signifies it
    represents a date. """
    return d.isdigit()


def text_to_date(date_string):
    return datetime.strptime(str(date_string), '%Y%m%d').date()


def copy_document(filename, doc_path):
    """ This moves a document from the intake point. to where this application
    expects it. Initally this is in a /static/ directory. Later it might be an
    S3 bucket. """

    destination = '/vagrant/code/krang/docusearch/static/docusearch/pdfs/'
    destination += filename
    shutil.copy2(doc_path, destination)
    return destination


def copy_and_extract_documents(agency_directory, d):
    date_dir = os.path.join(agency_directory, d)
    manifest_path = os.path.join(date_dir, 'manifest.yml')
    manifest = yaml.load(open(manifest_path, 'r'))

    for document in manifest:
        doc_filename = document['document']['document_id']
        doc_path = os.path.join(date_dir, doc_filename)
        doc_path = copy_document(doc_filename, doc_path)
        text_path = convert_to_text(doc_filename, doc_path)
        text_contents = open(text_path, 'r').read()
        yield (document, doc_path, text_contents)


def convert_to_text(file_name, doc_path):
    """ Given a pdf, extract the text. We will later be a bit more
    sophisticated here. """

    file_name_base = file_name.split('.')[0]

    extracted_folder = '/vagrant/code/krang/docusearch/static/docusearch/pdfs/'
    extracted_file = os.path.join(extracted_folder, '%s.txt' % file_name_base)
    subprocess.check_call(['pdftotext', doc_path, extracted_file], shell=False)
    return extracted_file


def create_document(document, release_slug):
    details, doc_path, text_contents = document
    d = Document()
    d.text = text_contents

    if 'title' in details['document']:
        d.title = details['document']['title']
    if 'document_date' in details['document']:
        d.date = text_to_date(details['document']['document_date'])

    d.release_agency_slug = release_slug

    filename = os.path.basename(doc_path)
    doc_path = 'docusearch/pdfs/%s' % filename
    d.path = doc_path
    d.save()


def process_office(agency_directory, agency, office_name):
    office_directory = os.path.join(agency_directory, office_name)

    office_slug = '%s--%s' % (agency, office_name)

    for d in os.listdir(office_directory):
        for document in copy_and_extract_documents(office_directory, d):
            create_document(document, office_slug)


def process_agency_documents(agency_directory, agency, date_directory):
    for document in copy_and_extract_documents(
            agency_directory, date_directory):
        create_document(document, agency)


def process_agency(documents_directory, agency):
    agency_directory = os.path.join(documents_directory, agency)

    for d in os.listdir(agency_directory):
        if is_date(d):
            process_agency_documents(agency_directory, agency, d)
        else:
            process_office(agency_directory, agency, d)

class Command(BaseCommand):

    def handle(self, *args, **options):
        documents_directory = '/vagrant/data/responsive'
        agencies = os.listdir(documents_directory)

        for agency in agencies:
            process_agency(documents_directory, agency)
