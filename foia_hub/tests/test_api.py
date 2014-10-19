import json
from django.test import TestCase, Client
from foia_hub.models import Agency, Office

from foia_hub.api import agency_preparer, contact_preparer


class PreparerTests(TestCase):
    fixtures = ['agencies_test.json']

    def test_agency_preparer(self):
        agency = Agency(
            name='agency-name',
            description='agency-description',
            abbreviation='AN',
            slug='agency-slug')
        fields_preparer = agency_preparer()
        ap = fields_preparer.prepare(agency)
        self.assertEqual('agency-name', ap['name'])
        self.assertEqual('agency-description', ap['description'])
        self.assertEqual('AN', ap['abbreviation'])
        self.assertEqual('agency-slug', ap['slug'])

    def test_contact_preparer(self):
        agency = Agency.objects.get(slug='department-of-homeland-security')
        self.assertNotEqual(agency, None)

        fields_preparer = contact_preparer()
        ap = fields_preparer.prepare(agency)

        data = {
            'name': 'Department of Homeland Security',
            'person_name': 'Joe Bureaucrat', 
            'email': 'foia@hq.dhs.gov', 
            'phone': None, 
            'toll_free_phone': None, 
            'fax': '202-343-1743',
            'public_liaison_name': 'Joe Liaison',
            'public_liaison_email': 'liaison@email.gov',
            'public_liaison_phone': '202-555-5555', 
            'request_form_url': 'http://dhs.gov/xfoia/editorial_0579.html',
            'office_url': 'http://www.dhs.gov/freedom-information-act-foia',
            'address_line_1': 'Stop 1',
            'street': '245 Murray Lane, SW',
            'city': 'Washington',
            'state': 'DC',
            'zip_code': '20528'
        }
        self.assertEqual(ap, data)

class AgencyOfficeAPITests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json']

    def test_autocomplete(self):
        """ Test that the autocomplete API works, and also ensure the results
        are sorted by name """

        c = Client()
        response = c.get('/api/agencyoffice/autocomplete/')
        content = response.content
        content = json.loads(content.decode('utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(content))

        slugs = [a['slug'] for a in content]
        self.assertEqual([
            'department-of-commerce',
            'department-of-homeland-security'], slugs)

    def test_agency_contact(self):
        c = Client()
        response = c.get('/api/agencyoffice/contact/department-of-commerce/')
        self.assertEqual(200, response.status_code)
        content = response.content
        content = json.loads(content.decode('utf-8'))

        self.assertEqual(content['agency_name'], 'Department of Commerce')
        self.assertEqual(1, len(content['offices']))
        self.assertEqual(
            'department-of-commerce--census-bureau',
            content['offices'][0]['slug'])
