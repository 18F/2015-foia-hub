from django.test import TestCase

from foia_hub.models import Agency
from foia_hub.scripts.load_agency_contacts import add_reading_rooms


class LoadingTest(TestCase):
    fixtures = ['agencies_test.json']

    def test_add_reading_rooms(self):
        reading_room_links = [[
            'Electronic Reading Room', 'http://agency.gov/err/']]
        agency = Agency.objects.get(slug='department-of-homeland-security')
        agency = add_reading_rooms(agency, reading_room_links)
        agency.save()

        # Retrieve saved
        dhs = Agency.objects.get(slug='department-of-homeland-security')
        self.assertEqual(
            'Electronic Reading Room',
            dhs.reading_room_urls.all()[0].link_text)
        self.assertEqual(
            'http://agency.gov/err/',
            dhs.reading_room_urls.all()[0].url)
