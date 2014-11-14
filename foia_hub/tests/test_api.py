import json
from django.test import TestCase, Client
from foia_hub.models import Agency

from foia_hub.api import agency_preparer, contact_preparer


class PreparerTests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json']

    def test_agency_preparer(self):
        """ Test the preparer that deals with just the unique Agency fields.
        """

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
        self.maxDiff = None
        agency = Agency.objects.get(slug='department-of-homeland-security')
        self.assertNotEqual(agency, None)

        fields_preparer = contact_preparer()
        ap = fields_preparer.prepare(agency)

        data = {
            'name': 'Department of Homeland Security',
            'person_name': 'Joe Bureaucrat',
            'emails': ['foia@hq.dhs.gov'],
            'phone': None,
            'toll_free_phone': None,
            'fax': '202-343-1743',
            'public_liaison_name': 'Joe Liaison',
            'public_liaison_email': 'liaison@email.gov',
            'public_liaison_phone': '202-555-5555',
            'request_form_url': 'http://dhs.gov/xfoia/editorial_0579.html',
            'office_url': 'http://www.dhs.gov/freedom-information-act-foia',
            'address_lines': ['Stop 1'],
            'street': '245 Murray Lane, SW',
            'city': 'Washington',
            'state': 'DC',
            'zip_code': '20528'
        }
        self.assertEqual(ap, data)


class AgencyAPITests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json',
        'stats_test.json']

    def test_list(self):
        """ Test that listing agencies work, and also ensure that the results
        are sorted by name. """

        c = Client()
        response = c.get('/api/agency/')
        self.assertEqual(200, response.status_code)

        content = response.content
        content = json.loads(content.decode('utf-8'))
        self.assertEqual(2, len(content['objects']))
        slugs = [a['slug'] for a in content['objects']]
        self.assertEqual(
            ['department-of-commerce', 'department-of-homeland-security'],
            slugs)

    def test_detail(self):
        """ Check the detail view for an agency."""

        c = Client()
        response = c.get('/api/agency/department-of-homeland-security/')
        self.assertEqual(200, response.status_code)
        content = response.content
        content = json.loads(content.decode('utf-8'))
        self.assertEqual(content['name'], 'Department of Homeland Security')
        self.assertEqual(1, len(content['offices']))
        self.assertEqual(
            'department-of-homeland-security--federal-emergency-management-agency',
            content['offices'][0]['slug'])
        self.assertEqual(37.5,content['complex_processing_time'])
        self.assertEqual(11,content['simple_processing_time'])
