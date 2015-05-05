import os

from django.test import TestCase
from docusearch.scripts.document_importer import DocImporter
from docusearch.models import ImportLog

LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))


class ImportTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """ Setting up class to test internal functions """
        agency = 'national-archives-and-records-administration'
        documents_directory = os.path.join(LOCAL_PATH, 'fixtures/')
        cls._connection = DocImporter(
            documents_directory=documents_directory, agency=agency)

    def test_is_date(self):
        """ For our specific use-case, a string contains a date if it's all
        numbers. Test if function is_date() correctly identifies dates. """

        self.assertTrue(self._connection.is_date('20140533'))
        self.assertFalse(self._connection.is_date('office-information-policy'))

    def test_unprocessed_directory(self):
        """ Check that unprocessed_directory function correctly verifies
        processed agency-date directories """

        # Check that agency folders work
        self.assertTrue(self._connection.unprocessed_directory('20150301'))
        il = ImportLog()
        il.agency_slug = self._connection.agency
        il.directory = '20150301'
        il.save()
        self.assertFalse(self._connection.unprocessed_directory('20150301'))

        # Check that office folders also work
        self._connection.agency = 'department-of-agriculture'
        self._connection.office = 'farmers-markets-desk'
        self.assertTrue(self._connection.unprocessed_directory('20140212'))
        office_il = ImportLog()
        office_il.agency_slug = 'department-of-agriculture'
        office_il.office_slug = 'farmers-markets-desk'
        office_il.directory = '20140212'
        office_il.save()
        self.assertFalse(self._connection.unprocessed_directory('20140212'))

        # Return DocImporter to original agency and office
        self._connection.agency = 'national-archives'
        self._connection.agency += '-and-records-administration'
        self._connection.office = None

    def test_mark_directory_processed(self):
        self.assertTrue(self._connection.unprocessed_directory('20150302'))
        self._connection.mark_directory_processed('20150302')
        self.assertFalse(self._connection.unprocessed_directory('20150302'))

    def test_import_log_decorator(self):
        """ Test that the import log decorator only lets an action happen once,
        and populates the database correctly.  """

        filler = []

        def process_documents():
            """ A fake process script """
            for x in range(1, 10):
                filler.append(x)

        self._connection.import_log_decorator('20130102', process_documents)
        self.assertEqual(filler, [1, 2, 3, 4, 5, 6, 7, 8, 9])

        self._connection.import_log_decorator('20130102', process_documents)
        self.assertEqual(filler, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_create_basic_document(self):
        doc_details = {
            'title': 'UFOs land on South Lawn',
            'document_date': '19500113',
            'file_type': 'pdf'
        }

        text_contents = "We are not alone."
        doc_tuple = (doc_details, None, text_contents)
        document = self._connection.create_basic_document(
            doc_tuple, 'state-department')
        self.assertEqual(document.title, 'UFOs land on South Lawn')
        self.assertEqual(document.text, 'We are not alone.')
