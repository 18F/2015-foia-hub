import os
import tempfile
import yaml

from boto.s3.key import Key
from django.core.files import File
from docusearch.models import Document, ImportLog


class DocImporter:

    def __init__(self, documents_directory, agency, office=None):

        self.documents_directory = documents_directory
        self.agency = agency
        self.office = office

        self.local_dir = self.agency
        if self.office:
            self.local_dir = self.office

    def is_date(self, d):
        """ If 'd' is all digits, return True as in our system this
        signifies it represents a date. """
        return d.isdigit()

    def agency_iterator(self):
        """ Loops through folders inside of a agency documents in a local
        directory """
        agency_directory = os.path.join(
            self.documents_directory, self.local_dir)
        for date_dir in os.listdir(agency_directory):
            yield date_dir

    def get_manifest_data(self, date_directory):
        """ Opens manifest and returns the manifest data along with path
        where the documents are located """
        documents_path = os.path.join(
            self.documents_directory, self.local_dir, date_directory)
        manifest_path = os.path.join(documents_path, 'manifest.yaml')
        return yaml.load(open(manifest_path, 'r')), documents_path

    def unprocessed_directory(self, date_directory):
        """ If we've completely processed a directory of documents, we will
        have an ImportLog entry for it. Return False if this is the case. """
        existing_logs_count = ImportLog.objects.filter(
            agency_slug=self.agency,
            office_slug=self.office,
            directory=date_directory).count()
        return existing_logs_count == 0

    def mark_directory_processed(self, date_directory):
        """ This simply creates an ImportLog entry, marking date_directory as
        having been processed for this agency/office combination. """
        il = ImportLog(
            agency_slug=self.agency,
            office_slug=self.office,
            directory=date_directory,
        )
        il.save()

    def get_raw_document(self, doc_path):
        """ Given a document path opens the document and returns the
        filename """
        doc_file = File(open(doc_path, 'rb'))
        filename = os.path.basename(doc_path)
        return doc_file, filename

    def create_document(self, document, release_slug):
        """ Create a Document object representing the document. This
        also uploads the document into it's S3 location. """
        d = self.create_basic_document(document, release_slug)
        d.save()
        details, doc_path, text_contents = document
        doc_file, filename = self.get_raw_document(doc_path)
        return d, filename, doc_file

    def create_basic_document(self, document, release_slug):
        """ Create a basic Document object (without the file upload
        related bits) """

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
        d.file_type = file_type

        return d

    def open_text_content(self, text_path):
        """ Opens a text document and returns text as string """
        return open(text_path, 'r').read()

    def get_documents(self, date_directory):
        """ Extract text from documents, and return a tuple contain
        documentation details and the extracted text. This function assumes
        that the text has been extracted"""
        manifest, documents_path = self.get_manifest_data(date_directory)
        for document in manifest:
            doc_path = os.path.join(documents_path, document['doc_location'])
            root, ext = os.path.splitext(doc_path)
            text_contents = self.open_text_content(root + '.txt')
            yield (document, doc_path, text_contents)

    def import_log_decorator(self, date_directory, process_documents):
        """ Runs the `process_documents` to ingest documents only if the
        directory has not been processed """
        if self.unprocessed_directory(date_directory):
            process_documents()
            self.mark_directory_processed(date_directory)

    def process_date_documents(self, date_directory):
        """ Creates correct agency/office slug and starts the import process
        for a specific date directory """
        release_slug = self.agency
        if self.office:
            release_slug = '%s-%s' % (release_slug, self.office)

        def process():
            for document in self.get_documents(date_directory):
                d, filename, doc = self.create_document(document, release_slug)
                d.original_file.save(filename, doc, save=True)

        self.import_log_decorator(date_directory, process)

    def new_processor(self, office):
        """ Spawn a child of the same class """
        new_location = os.path.join(self.documents_directory, self.agency)
        return DocImporter(new_location, self.agency, office)

    def import_docs(self):
        """ An Agency directory can either have sub-Office directories, or date
        named directories that contain actual documents. This processes both
        appropriately. """
        for date_dir in self.agency_iterator():
            if self.is_date(date_dir):
                self.process_date_documents(date_dir)
            else:
                office_processor = self.new_processor(date_dir)
                office_processor.import_docs()


class DocImporterS3(DocImporter):

    def __init__(self, s3_bucket, agency, office=None):
        self.s3_bucket = s3_bucket
        documents_directory = ''
        super().__init__(documents_directory, agency, office)

        self.local_dir = self.agency
        if self.office:
            self.local_dir = os.path.join(self.local_dir, self.office)

    def last_name_in_path(self, path):
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

    def agency_iterator(self):
        """ Loops through folders inside of a agency folder """
        agency_directory = self.s3_bucket.list(self.local_dir + '/', "/")
        for date_dir in agency_directory:
            yield self.last_name_in_path(date_dir.name)

    def get_manifest_data(self, date_directory):
        """ Opens manifest and returns the manifest data along with path
        where the documents are located """
        documents_path = os.path.join(
            self.documents_directory, self.local_dir, date_directory)
        manifest_path = os.path.join(documents_path, 'manifest.yaml')
        k = Key(self.s3_bucket)
        k.key = manifest_path
        return yaml.load(k.get_contents_as_string()), documents_path

    def open_text_content(self, text_path):
        """ Opens a text document from s3 and returns text as string """
        k = Key(self.s3_bucket)
        k.key = text_path
        return k.get_contents_as_string()

    def new_processor(self, office):
        """ Spawn a child of the same class """

        return DocImporterS3(self.s3_bucket, self.agency, office)

    def get_raw_document(self, doc_path):
        """ Returns the document file and file name """
        filename = os.path.basename(doc_path)
        with tempfile.TemporaryDirectory() as tmpdirname:
            k = Key(self.s3_bucket)
            k.key = doc_path
            temp_path = os.path.join(tmpdirname, filename)
            k.get_contents_to_filename(temp_path)
            doc_file = File(open(temp_path, 'rb'))
        return doc_file, filename
