import json
from django.test import TestCase, Client
from foia_hub.models import Agency, Office

from foia_hub.api import agency_preparer, office_preparer


class PreparerTests(TestCase):
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

    def test_office_preparer(self):
        agency = Agency(
            name='agency-name',
            description='agency-description',
            abbreviation='AN',
            slug='agency-slug')
        office = Office(
            name='office-name',
            slug='office-slug',
            agency=agency)
        fields_preparer = office_preparer()
        op = fields_preparer.prepare(office)
        self.assertEqual('office-name', op['name'])
        self.assertEqual('agency-slug--office-slug', op['slug'])


class AgencyOfficeAPITests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json']

    def test_autocomplete(self):
        c = Client()
        response = c.get('/api/agencyoffice/autocomplete/')
        content = response.content
        content = json.loads(content.decode('utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(4, len(content))

        slugs = [a['slug'] for a in content]
        slugs.sort()
        fema-slug = 'department-of-homeland-security'
        fema_slug += '--federal-emergency-management-agency'
        self.assertEqual([
            'department-of-commerce',
            'department-of-commerce--census-bureau',
            'department-of-homeland-security',
            fema-slug], slugs)

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
