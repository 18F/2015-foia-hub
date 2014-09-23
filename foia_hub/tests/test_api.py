from django.test import TestCase
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
        office = Office(
            name='office-name',
            slug='office-slug')
        fields_preparer = office_preparer()
        op = fields_preparer.prepare(office)
        self.assertEqual('office-name', op['name'])
        self.assertEqual('office-slug', op['slug'])
