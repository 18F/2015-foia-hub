from django.test import TestCase

from foia_hub.models import Agency
from foia_hub.scripts.load_agency_contacts import add_reading_rooms,\
    get_latest_stats, add_request_time_statistics


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

    def test_get_latest_stats(self):
        """ Confirms that latest stats available are returned """
        data = {'request_time_stats': {
            '2011': {'simple_median_days': '1'},
            '2012': {'complex_median_days': '2'},
            '2013': {'simple_median_days': '3'},
            '2014': {'complex_median_days': '4'}}}
        iterator = [('S', 'simple'), ('C', 'complex')]
        latest_stats = get_latest_stats(data, iterator, {})
        self.assertEqual({'S': '3', 'C': '4'}, latest_stats)

    def test_add_stats(self):
        """ Confirms all latest records are loaded and no empty records
        are created """
        # Load data
        agency = Agency.objects.get(slug='department-of-homeland-security')
        data = {'request_time_stats': {
            '2012': {'simple_median_days': '2'},
            '2014': {'simple_median_days': '21'}}}
        add_request_time_statistics(data, agency)

        # Verify latest data is returned when it exists
        retrieved = agency.stats_set.filter(
            stat_type='S').order_by('-year').first()
        self.assertEqual(retrieved.median, 21)

        # Verify that no empty records are created
        retrieved = agency.stats_set.filter(
            stat_type='C').order_by('-year').first()
        self.assertEqual(retrieved, None)
        with self.assertRaises(AttributeError) as error:
            retrieved.median
        self.assertEqual(type(error.exception), AttributeError)
