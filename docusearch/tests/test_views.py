from django.core.urlresolvers import reverse
from django.test import TestCase

from docusearch.templatetags.generate_get_req import generate_get_req


class TestViews(TestCase):

    def test_home_page(self):
        """ The /document/search/ page should load without errors. """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "search and find documents released")


class TestTemplateTags(TestCase):

    def test_generate_get_req(self):
        """ Test that the parameter generator works properly """

        original_data = [('q', 'testquery')]
        expected_data = '?q=testquery'
        self.assertEqual(generate_get_req(original_data), expected_data)

        original_data.append(('order_by', 'relevance'))
        expected_data = '?q=testquery&order_by=relevance'
        self.assertEqual(generate_get_req(original_data), expected_data)
