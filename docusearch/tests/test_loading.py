from django.test import TestCase

from docusearch.management.commands import import_documents as importer

from docusearch.models import ImportLog


class ImportTest(TestCase):

    def test_is_date(self):
        """ For our specific use-case, a string contains a date if it's all
        numbers. Test if function is_date() correctly identifies dates. """

        self.assertTrue(importer.is_date('20140533'))
        self.assertFalse(importer.is_date('office-information-policy'))

    def test_text_to_date(self):
        """ Test our simple function that turns a string into a date object.
        """

        d = importer.text_to_date('20140215')
        self.assertEqual(2014, d.year)
        self.assertEqual(2, d.month)
        self.assertEqual(15, d.day)

    def test_unprocessed_directory(self):
        self.assertTrue(importer.unprocessed_directory(
            '20150301', 'department-of-justice'))

        il = ImportLog()
        il.agency_slug = 'department-of-justice'
        il.directory = '20150301'
        il.save()

        self.assertFalse(importer.unprocessed_directory(
            '20150301', 'department-of-justice'))

        self.assertTrue(importer.unprocessed_directory(
            '20140212-1', 'department-of-agriculture', 'farmers-markets-desk'))

        office_il = ImportLog()
        office_il.agency_slug = 'department-of-agriculture'
        office_il.office_slug = 'farmers-markets-desk'
        office_il.directory = '20140212-1'
        office_il.save()

        self.assertFalse(importer.unprocessed_directory(
            '20140212-1', 'department-of-agriculture', 'farmers-markets-desk'))

    def test_mark_directory_processed(self):
        self.assertTrue(importer.unprocessed_directory(
            '20150302', 'department-of-defense'))
        importer.mark_directory_processed('20150302', 'department-of-defense')
        self.assertFalse(importer.unprocessed_directory(
            '20150302', 'department-of-defense'))

    def test_import_log_decorator(self):
        """ Test that the import log decorator only lets an action happen once,
        and populates the database correctly.  """

        filler = []

        def process_documents():
            """ A fake process script """
            for x in range(1, 10):
                filler.append(x)

        importer.import_log_decorator(
            '20130102', 'cfpb', None, process_documents)
        self.assertEqual(filler, [1, 2, 3, 4, 5, 6, 7, 8, 9])

        importer.import_log_decorator(
            '20130102', 'cfpb', None, process_documents)
        self.assertEqual(filler, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_create_basic_document(self):
        doc_details = {
            'title': 'UFOs land on South Lawn',
            'document_date': '19500113',
            'file_type': 'pdf'
        }

        text_contents = "We are not alone."
        doc_tuple = (doc_details, None, text_contents)
        document = importer.create_basic_document(
            doc_tuple, 'state-department')
        self.assertEqual(document.title, 'UFOs land on South Lawn')
        self.assertEqual(document.text, 'We are not alone.')
