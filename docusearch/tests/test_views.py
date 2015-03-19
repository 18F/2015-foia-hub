from django.core.urlresolvers import reverse
from django.test import TestCase

from docusearch.templatetags.get_filename import get_filename


class TestViews(TestCase):

    def test_home_page(self):
        """ The /document/search/ page should load without errors. """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "search and find documents released")


class TestTemplateTags(TestCase):

    def test_get_filename(self):
        """ Test the function extract filename correctly """

        original_data = '/filepath/filepath/filename.txt'
        expected_data = 'filename.txt'
        self.assertEqual(get_filename(original_data), expected_data)
