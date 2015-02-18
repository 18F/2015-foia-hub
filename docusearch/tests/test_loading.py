from django.test import TestCase

from docusearch.management.commands import import_documents as importer


class ImportTest(TestCase):

    def test_is_date(self):
        """ For our specfic use-case, a string contains a date if it's all
        numbers. Let's test that. """

        self.assertTrue(importer.is_date('20140533'))
        self.assertFalse(importer.is_date('office-information-policy'))

    def test_text_to_date(self):
        """ Test our simple function that turns a string into a date object.
        """

        d = importer.text_to_date('20140215')
        self.assertEqual(2014, d.year)
        self.assertEqual(2, d.month)
        self.assertEqual(15, d.day)
