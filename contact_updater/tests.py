from django.test import TestCase
from django.core.urlresolvers import reverse
from contact_updater import views


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


class HelpFunctionTests(TestCase):

    def test_get_first_array(self):
        """ Test that first element of array is returned"""

        # Array with one element
        self.assertEqual(views.get_first_element([1]), 1)

        # Array with multiple elements
        self.assertEqual(views.get_first_element([1, 2, 3]), 1)

        # Array with no elments
        self.assertEqual(views.get_first_element([]), None)

    def test_unpack_libraries(self):
        """ Validate that libraries dicts are unpacked correctly """

        library_dict = [
            {
                'link_text': 'FOIA Electronic Reading Room',
                'url': 'http://www.dhs.gov/foia-library'
            }
        ]
        expected_output = 'http://www.dhs.gov/foia-library'

        # Test one library
        self.assertEqual(views.unpack_libraries(library_dict), expected_output)

        library_dict.append(
            [
                {
                    'link_text': 'FOIA Electronic Reading Room',
                    'url': 'http://www.dhs.gov/foia-library-2'
                }
            ])
        expected_output = 'http://www.dhs.gov/foia-library'
        # Test more than one library
        self.assertEqual(views.unpack_libraries(library_dict), expected_output)

        # Test no libraries
        self.assertEqual(views.unpack_libraries([]), None)

    def test_join_array(self):
        """ Validate the array is joined using `\n` """

        test_data = ['1', '2', '3']
        expected_output = '1\n\2\n\3'

        # Test multiple array elements
        self.assertEqual(views.join_array(test_data, expected_output))

        # Tests no array elements
        self.assertEqual(views.join_array([]), None)
