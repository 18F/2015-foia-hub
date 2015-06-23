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
        self.assertContains(response, 'Update your')


class FormPageTests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json']

    def test_centralized_form_get(self):
        """ Make sure the form populates correctly """

        response = self.client.get(
            reverse(
                'contact_updater_form',
                kwargs={'slug': 'us-patent-and-trademark-office'}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'form_selector')

    def test_decentralized_form_get(self):
        """ Make sure the form populates correctly """

        response = self.client.get(
            reverse(
                'contact_updater_form',
                kwargs={'slug': 'department-of-commerce'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form_selector')


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
        self.assertEqual(views.unpack_libraries([]), '')

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

    def test_prepare_address_lines(self):
        """ Checks that address lines are coverted to a dict containing
        two keys address_line_1, which contains the first element in the
        address lines array and address_line_2, which contains the rest of the
        elements """
        # Testing 0 lines
        address_lines = []
        data = views.prepare_address_lines(lines=address_lines)
        self.assertEqual({}, data)

        # Testing 1 line
        address_lines.append('line 1')
        data = views.prepare_address_lines(lines=address_lines)
        self.assertEqual({'address_line_1': 'line 1'}, data)

        # Testing 2 lines
        address_lines.append('line 2')
        data = views.prepare_address_lines(lines=address_lines)
        self.assertEqual(
            {'address_line_1': 'line 1', 'address_line_2': 'line 2'}, data)

        # Testing 3 lines
        address_lines.append('line 3')
        data = views.prepare_address_lines(lines=address_lines)
        self.assertEqual(
            {'address_line_1': 'line 1', 'address_line_2': 'line 2 line 3'},
            data)

    def test_prepare_emails(self):
        """ Check if function returns only the first email, else returns
        a blank line """
        # Test with no emails
        emails = []
        data = views.prepare_emails(emails)
        self.assertEqual(data, {'emails': ''})

        # Test with 1 email
        emails.append('test@gmail.com')
        data = views.prepare_emails(emails)
        self.assertEqual(data, {'emails': 'test@gmail.com'})

        # Test with 2 email
        emails.append('test_2@gmail.com')
        data = views.prepare_emails(emails)
        self.assertEqual(data, {'emails': 'test@gmail.com'})
