from django.core.urlresolvers import reverse
from django.test import TestCase

from docusearch.templatetags.get_filename import get_filename
from docusearch.templatetags.remove_from_query import remove_from_query


class TestViews(TestCase):

    fixtures = ['documents.json']

    def test_home_page(self):
        """ The /document/search/ page should load without errors. """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Improving the FOIA request")

    def test_search(self):
        """ Document search should work properly """

        # Empty search returns nothing, but won't fail
        response = self.client.get(reverse('doc_search') + '?q=')
        self.assertEqual(response.status_code, 200)

    def test_details(self):
        """ Document details should return document """
        response = self.client.get('/documents/document/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Interim Report to Congress")
        # Details contain link to FOIA contacts
        self.assertContains(
            response,
            '/contacts/department-of-justice--office-of-information-policy'
        )


class TestTemplateTags(TestCase):

    def test_get_filename(self):
        """ Test the function extract filename correctly """

        original_data = '/filepath/filepath/filename.txt'
        expected_data = 'filename.txt'
        self.assertEqual(get_filename(original_data), expected_data)

        original_data = ''
        expected_data = 'Document'
        self.assertEqual(get_filename(original_data), None)

    def test_remove_from_query(self):
        """ Test that the remove query template tag removes the
        correct query """

        query = 'q=test&test=q'
        new_query = remove_from_query(query, ['q'])
        self.assertEqual(new_query, 'test=q')
