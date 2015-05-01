from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File

import yaml
import os
import tempfile

from .document_importer import is_date
from .import_documents import unprocessed_directory, mark_directory_processed
from .import_documents import create_basic_document


def last_name_in_path(path):
    """
    Returns the last name in a path.

    'doc/20150301/' returns 20150301
    'doc/20150301/abc.pdf' returns abc.pdf
    """
    path_split = path.rsplit('/')

    if path_split[-1] == '':
        return path_split[-2]
    else:
        return path_split[-1]


class Command(BaseCommand):

    help = """Import documents from your document source S3 bucket, into
    docusearch. """

    def import_log_decorator(self, date_directory, agency,
                             office, process_documents):
        if unprocessed_directory(date_directory, agency, office):
            process_documents()
            mark_directory_processed(date_directory, agency, office)

    def read_manifest(self, directory_prefix):
        """ Given the path to an agency's date directory, return a parsed
        manifest file if it exists. """

        manifest_name = directory_prefix.name + 'manifest.yaml'
        manifest_key = directory_prefix.bucket.get_key(manifest_name)

        if manifest_key:
            manifest = yaml.load(manifest_key.get_contents_as_string())
            return manifest

    def copy_and_extract_documents(self, date_directory,
                                   directory_prefix, manifest):
        """ Extract text from documents, and return a tuple contain documentation
        details and the extracted text. """

        for document in manifest:
            doc_path = os.path.join(
                directory_prefix.name, document['doc_location'])
            root, ext = os.path.splitext(doc_path)
            k = Key(self.bucket)
            k.key = root + ".txt"
            text_contents = k.get_contents_as_string()
            yield(document, doc_path, text_contents)

    def create_document(self, document, release_slug):
        """ Create a Document object representing the document.
        This also uploads the document into it's S3 location. """

        d = create_basic_document(document, release_slug)
        details, doc_path, text_contents = document

        filename = os.path.basename(doc_path)

        with tempfile.TemporaryDirectory() as tmpdirname:
            k = Key(self.bucket)
            k.key = doc_path
            temp_path = os.path.join(tmpdirname, filename)
            k.get_contents_to_filename(temp_path)
            doc_file = File(open(temp_path, 'rb'))
            print('new doc')
            d.original_file.save(filename, doc_file, save=True)

    # we might want to rename this to: "read_manifest"
    def process_date_documents(self, agency, date_directory, directory_prefix):
        """
        agency example: 'department-of-commerce/'

        date_directory: '20150331'

        directory_prefix: boto.s3.prefix.Prefix object. directory_prefix.name
        returns '/department-of-commerce/20150331/'
        """
        release_slug = agency

        manifest = self.read_manifest(directory_prefix)

        def process():
            for document in self.copy_and_extract_documents(
                    date_directory, directory_prefix, manifest):
                self.create_document(document, release_slug)

        self.import_log_decorator(date_directory, agency, None, process)

    def handle(self, *args, **options):

        aws_connection = S3Connection(
            settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        self.bucket = aws_connection.get_bucket(settings.DOCS_SOURCE_BUCKET)

        rs = self.bucket.list("", "/")

        for key in rs:
            agency = key.name

            ts = self.bucket.list(agency, "/")
            for asd in ts:
                agency_sub_directory = last_name_in_path(asd.name)
                if is_date(agency_sub_directory):
                    self.process_date_documents(
                        agency, agency_sub_directory, asd)
