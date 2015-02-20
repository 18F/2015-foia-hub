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
