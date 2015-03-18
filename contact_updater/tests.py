from django.test import TestCase
from django.core.urlresolvers import reverse

from contact_updater import views


api_data = {
    'offices': [],
    'public_liaison_email': None,
    'foia_libraries': [{'url': 'http://www.amtrak.com/library'}],
    'simple_processing_time': 1.0,
    'name': 'AMTRAK',
    'common_requests': [],
    'phone': '202-906-3741',
    'abbreviation': 'NRPC',
    'request_form_url': None,
    'agency_slug': 'amtrak',
    'state': 'DC',
    'slug': 'amtrak',
    'description': 'Test Description',
    'toll_free_phone': None,
    'complex_processing_time': 13.5,
    'no_records_about': ['test 1', 'test 2'],
    'street': '60 Massachusetts Avenue, NE',
    'agency_name': 'AMTRAK',
    'zip_code': '20002',
    'person_name': None,
    'office_url': 'http://www.amtrak.com/test',
    'keywords': None,
    'emails': ['foiarequests@amtrak.com', 'foiarequests@amtrak.com'],
    'address_lines': ['Sharron H. Hawkins', 'FOIA Officer'],
    'is_a': 'agency',
    'public_liaison_name': 'Sharron H. Hawkins',
    'public_liaison_phone': '202-906-3740',
    'city': 'Washington', 'fax': '202-906-3285'
}


class MainPageTests(TestCase):
    fixtures = ['agencies_test.json']

    def test_main_page(self):
        """ The main page should load without errors. """

        response = self.client.get(reverse('contact_updater_index'))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        self.assertTrue('department-of-commerce' in content)


class FormPageTests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json']

    def test_form_page_get(self):
        """ Make sure the form populates correctly """

        response = self.client.get(
            reverse(
                'contact_updater_form',
                kwargs={'slug': 'department-of-commerce'}))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        self.assertTrue('<h2>Department of Commerce</h2>' in content)


class HelpFunctionTests(TestCase):

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
        expected_output = '\n'.join(test_data)

        # Test multiple array elements
        self.assertEqual(views.join_array(test_data), expected_output)

        # Tests no array elements
        self.assertEqual(views.join_array([]), None)

    def test_transform_data(self):
        """
        Checks that data is transformed into usable format for form correctly
        """
        transformed_data = views.transform_data(api_data)

        self.assertEqual(
            transformed_data.get('emails'), 'foiarequests@amtrak.com')
        self.assertEqual(
            transformed_data.get('foia_libraries'),
            'http://www.amtrak.com/library')
        self.assertEqual(
            transformed_data.get('common_requests'),
            None)
        self.assertEqual(
            transformed_data.get('no_records_about'),
            '\n'.join(['test 1', 'test 2']))
        self.assertEqual(
            transformed_data.get('address_lines'),
            '\n'.join(['Sharron H. Hawkins', 'FOIA Officer']))
