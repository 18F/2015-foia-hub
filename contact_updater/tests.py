from django.test import TestCase
from django.core.urlresolvers import reverse


class MainPageTests(TestCase):

    def test_main_page(self):
        """ The main page should load without errors. """
        # Main page loads from external api can we send it a mock?
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        self.assertTrue('department-of-the-treasury' in content)


class FormPageTests(TestCase):

    def test_form_page(self):
        """ Make sure the form populates correctly """

        response = self.client.get(reverse('form', kwargs={'slug': 'amtrak'}))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        self.assertTrue('<h2>AMTRAK</h2>' in content)
