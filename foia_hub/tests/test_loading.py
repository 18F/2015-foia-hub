from django.test import TestCase

from foia_hub.models import Agency, Office
from foia_hub.scripts.load_agency_contacts import (
    load_data, update_reading_rooms, add_request_time_statistics,
    extract_tty_phone, extract_non_tty_phone, build_abbreviation)


example_office1 = {
    'address': {
        'address_lines': ['line 1', 'line 2'],
        'street': '75 Hawthorne Street',
        'city': 'San Francisco',
        'state': 'CA',
        'zip': '94105'
    },
    'emails': ['williams.deborah@epa.gov'],
    'keywords': ['keyword 1', 'keyword 2'],
    'misc': {'U.S. EPA, Region 9': 'Regional Freedom of Information\
        Officer, Phone: 415-947-4251'},
    'name': 'Region 9 (States: AZ, CA, HI, NV, AS, GU)',
    'phone': '415-947-4251',
    'public_liaison': {'name': 'Deborah Williams', 'phone': ['703-516-5555']},
    'request_form': 'http://www.epa.gov/foia/requestform.html',
    'service_center': {'name': 'Timbo Two', 'phone': ['415-947-4251']},
    'top_level': False,
    'website': 'http://www.epa.gov/region09/foia/index.html'
}

example_sub_office = {
    'abbreviation': 'R9',
    'address': {
        'address_lines': ['line 1', 'line 2'],
        'street': '75 Hawthorne Street',
        'city': 'San Francisco',
        'state': 'CA',
        'zip': '94105'
    },
    'emails': ['williams.deborah@epa.gov'],
    'common_requests': ['common request 1'],
    'description': 'The mission of this sub is...',
    'keywords': ['keyword 1', 'keyword 2'],
    'misc': {'U.S. EPA, Region 10': 'Regional Freedom of Information\
        Officer, Phone: (415) 947-4251'},
    'name': 'Region 10 (States: AK, ID, OR, WA)',
    'no_records_about': ['no records about 1'],
    'phone': '415-947-4251',
    'public_liaison': {'name': 'Deborah Williams', 'phone': ['703-516-5555']},
    'request_form': 'http://www.epa.gov/foia/requestform.html',
    'service_center': {'name': 'Timbo', 'phone': ['415-947-4251']},
    'top_level': True,
    'website': 'http://www.epa.gov/region09/foia/index.html'
}

example_agency = {
    'abbreviation': 'EPA',
    'address': {
        'address_lines': [
            'Larry Gottesman',
            'National Freedom of Information Officer',
            '(2882T)'],
        'street': '1200 Pennsylvania Avenue, NW',
        'city': 'Washinton',
        'state': 'DC',
        'zip': '20460'
    },
    'common_requests': ['common request 1'],
    'departments': [example_office1, example_sub_office],
    'description': 'The mission of EPA is to protect',
    'keywords': ['Acid Rain', 'Agriculture'],
    'name': 'Environmental Protection Agency',
    'no_records_about': ['no records about 1'],
}


class LoaderTest(TestCase):
    def test_load_data(self):
        """ Check that agency data is loaded correctly """

        load_data(example_agency)

        # Check that agency elements are loaded
        a = Agency.objects.get(name='Environmental Protection Agency')
        self.assertEqual('environmental-protection-agency', a.slug)
        self.assertEqual('The mission of EPA is to protect', a.description)
        self.assertEqual(['Acid Rain', 'Agriculture'], a.keywords)
        self.assertEqual(['common request 1'], a.common_requests)
        self.assertEqual(['no records about 1'], a.no_records_about)

        # Check that elements from top-level (sub_agency) offices are loaded
        sub_a = Agency.objects.get(
            name='Region 10 (States: AK, ID, OR, WA)')
        self.assertEqual(
            'region-10-states-ak-id-or-wa', sub_a.slug)
        self.assertEqual(['keyword 1', 'keyword 2'], sub_a.keywords)
        self.assertEqual(a, sub_a.parent)
        # Ensure that abbreviations are not overwritten
        self.assertEqual('R9', sub_a.abbreviation)
        self.assertEqual(['common request 1'], sub_a.common_requests)
        self.assertEqual(['no records about 1'], sub_a.no_records_about)
        self.assertEqual(
            'The mission of this sub is...', sub_a.description)

        # Check that elements from regular offices are loaded
        o = Office.objects.get(
            name='Region 9 (States: AZ, CA, HI, NV, AS, GU)')
        self.assertEqual(
            'environmental-protection-agency-' +
            '-region-9-states-az-ca-hi-nv-as-gu', o.slug)

    def test_multi_load(self):
        """ Ensures that old data are set to null on second load """

        # Load one
        load_data(example_agency)
        sub_a = Agency.objects.get(
            name='Region 10 (States: AK, ID, OR, WA)')
        self.assertEqual(sub_a.person_name, 'Timbo')
        self.assertEqual(sub_a.public_liaison_name, 'Deborah Williams')
        self.assertEqual(sub_a.address_lines, ['line 1', 'line 2'])
        self.assertEqual(sub_a.zip_code, '94105')
        self.assertEqual(sub_a.state, 'CA')
        self.assertEqual(sub_a.city, 'San Francisco')
        self.assertEqual(sub_a.street, '75 Hawthorne Street')

        # Deleting values
        del (example_sub_office['service_center']['name'],
             example_sub_office['public_liaison']['name'],
             example_sub_office['address']['address_lines'],
             example_sub_office['address']['zip'],
             example_sub_office['address']['state'],
             example_sub_office['address']['city'],
             example_sub_office['address']['street']
             )

        # Load two test
        load_data(example_agency)
        sub_a = Agency.objects.get(
            name='Region 10 (States: AK, ID, OR, WA)')
        self.assertEqual(sub_a.person_name, None)
        self.assertEqual(sub_a.public_liaison_name, None)
        self.assertEqual(sub_a.address_lines, [])
        self.assertEqual(sub_a.zip_code, None)
        self.assertEqual(sub_a.state, None)
        self.assertEqual(sub_a.city, None)
        self.assertEqual(sub_a.street, None)


class LoadingTest(TestCase):

    fixtures = ['agencies_test.json', 'offices_test.json']

    def test_update_reading_rooms(self):
        """ Test if reading rooms are added properly """

        reading_room_data = {
            'reading_rooms': [
                ['Electronic Reading Room', 'http://agency.gov/err/'],
                ['Pre-2000 Reading Room', 'http://agency.gov/pre-2000/rooms']]
        }
        agency = Agency.objects.get(slug='department-of-homeland-security')
        update_reading_rooms(agency, reading_room_data)
        agency.save()

        # Retrieve saved
        dhs = Agency.objects.get(slug='department-of-homeland-security')
        self.assertEqual(2, len(dhs.reading_room_urls.all()))
        reading_room_1 = dhs.reading_room_urls.get(
            link_text='Electronic Reading Room')
        self.assertEqual(
            'Electronic Reading Room',
            reading_room_1.link_text)
        self.assertEqual(
            'http://agency.gov/err/',
            reading_room_1.url)
        reading_room_2 = dhs.reading_room_urls.get(
            link_text='Pre-2000 Reading Room')
        self.assertEqual(
            'Pre-2000 Reading Room',
            reading_room_2.link_text)
        self.assertEqual(
            'http://agency.gov/pre-2000/rooms',
            reading_room_2.url)

    def test_add_delete_reading_rooms(self):
        """ Add a reading room. Then, remove a reading room (by omission)
        during a subsequent load. The reading rooms in the database should
        reflect these changes (the removed reading room should not be there.
        """

        census = Office.objects.get(
            slug='department-of-commerce--census-bureau')
        all_rooms = census.reading_room_urls.all().count()
        self.assertEqual(0, all_rooms)

        data = {
            'reading_rooms': [
                ['Url One', 'http://urlone.gov'],
                ['Url Two', 'http://urltwo.gov']]}
        update_reading_rooms(census, data)
        all_rooms = census.reading_room_urls.all()
        self.assertEqual(2, len(all_rooms))

        data = {
            'reading_rooms': [
                ['Url One', 'http://urlone.gov'],
                ['Url Three', 'http://urlthree.gov']]}
        update_reading_rooms(census, data)
        rr_count = census.reading_room_urls.all().count()
        self.assertEqual(2, rr_count)

    def test_add_stats(self):
        """
        Confirms all latest records are loaded, no empty records
        are created, and records with a value of `less than one`
        are flagged.
        """
        # Load data
        agency = Agency.objects.get(slug='department-of-homeland-security')
        data = {'request_time_stats': {
            '2012': {'simple_median_days': '2'},
            '2014': {'simple_median_days': 'less than 1'}
        }}

        add_request_time_statistics(data, agency)

        # Verify that only one stat was added
        self.assertEqual(len(agency.stats_set.all()), 1)

        # Verify latest data is returned when it exists
        retrieved = agency.stats_set.filter(
            stat_type='S').order_by('-year').first()
        self.assertEqual(retrieved.median, 1)

        # Verify that `less than one` records are flagged
        retrieved = agency.stats_set.filter(
            stat_type='S').order_by('-year').first()
        self.assertEqual(retrieved.less_than_one, True)

        # Load test 2
        agency = Agency.objects.get(slug='department-of-homeland-security')
        data = {'request_time_stats': {
            '2015': {'simple_median_days': '3',
                     'complex_median_days': '3'}}}
        add_request_time_statistics(data, agency)

        # Verify latest old data is overwritten when new data is updated
        self.assertEqual(len(agency.stats_set.all()), 2)

    def test_extract_tty_phone(self):
        """ Test: from a service center entry, extract the TTY phone if it
        exists. """

        service_center = {
            'phone': ['202-555-5555 (TTY)', '202-555-5551']
        }

        tty_phone = extract_tty_phone(service_center)
        self.assertEqual('202-555-5555 (TTY)', tty_phone)

        service_center['phone'] = ['202-555-5551']
        tty_phone = extract_tty_phone(service_center)
        self.assertEqual(None, tty_phone)

        service_center['phone'] = [
            '202-555-5555 (TTY)', '202-555-5552 (TTY)', '202-555-5551']
        tty_phone = extract_tty_phone(service_center)
        self.assertEqual('202-555-5555 (TTY)', tty_phone)

    def test_extract_non_tty_phone(self):
        """ Test that extract non-tty phone numbers from a list works. If there
        aren't any, this defaults to TTY numbers (and tests that)"""

        public_liaison = {
            'phone': ['202-555-5551', '202-555-5555 (TTY)']
        }

        phone = extract_non_tty_phone(public_liaison)
        self.assertEqual('202-555-5551', phone)

        # No non-tty number
        public_liaison['phone'] = ['202-555-5552 (TTY)']
        phone = extract_non_tty_phone(public_liaison)
        self.assertEqual('202-555-5552 (TTY)', phone)

        public_liaison['phone'] = []
        phone = extract_non_tty_phone(public_liaison)
        self.assertEqual(None, phone)

    def test_build_abbreviation(self):
        """ Test that abbreviations are built correctly """

        sub_agency_name = "Administrative Conference of the United States"
        self.assertEqual("ACUS", build_abbreviation(sub_agency_name))

        sub_agency_name = "U.S. Customs & Border Protection"
        self.assertEqual("USCBP", build_abbreviation(sub_agency_name))
