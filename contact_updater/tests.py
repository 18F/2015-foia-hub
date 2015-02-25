from django.test import TestCase
from django.core.urlresolvers import reverse


class MainPageTests(TestCase):
    fixtures = ['agencies_test.json']

    def test_main_page(self):
        """ The main page should load without errors. """
        # Main page loads from external api can we send it a mock?
        response = self.client.get(reverse('contact_updater_index'))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        self.assertTrue('department-of-commerce' in content)


class FormPageTests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json']

    def test_form_page(self):
        """ Make sure the form populates correctly """

        response = self.client.get(
            reverse(
                'contact_updater_form',
                kwargs={'slug': 'department-of-commerce'}))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        self.assertTrue('<h2>Department of Commerce</h2>' in content)
