import json
from django.db import connection
from django.test import TestCase, Client
from django.utils.unittest import skipIf, skipUnless

from foia_hub.models import Agency, ReadingRoomUrls, Office

from foia_hub.api import agency_preparer, contact_preparer
from foia_hub.api import foia_libraries_preparer
from foia_hub.api import sanitize_search_term, dictfetchall
from foia_hub.tests import helpers


from foia_hub.settings.test import custom_backend


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

    @skipIf(custom_backend == 'postgresql_psycopg2',
            'The order of the returned data changes with postgres')
    def test_reading_room_preparer(self):
        """ Ensure reading room urls are serialized correctly. """

        census = Office.objects.get(
            slug='department-of-commerce--census-bureau')

        rone = ReadingRoomUrls(
            content_object=census,
            link_text='Url One',
            url='http://urlone.gov')
        rone.save()
        rtwo = ReadingRoomUrls(
            content_object=census,
            link_text='Url Two',
            url='http://urltwo.gov')
        rtwo.save()

        data = foia_libraries_preparer(census)

        serialized_rooms = {'foia_libraries': [
            {'link_text': 'Url One', 'url': 'http://urlone.gov'},
            {'link_text': 'Url Two', 'url': 'http://urltwo.gov'}]}

        self.assertEqual(serialized_rooms, data)


class AgencyAPITests(TestCase):
    fixtures = [
        'agencies_test.json', 'offices_test.json', 'stats_test.json']

    def test_list(self):
        """ Test that listing agencies work, and also ensure that the results
        are sorted by name. """

        c = Client()
        response = c.get('/api/agency/')
        self.assertEqual(200, response.status_code)

        content = response.content
        content = json.loads(content.decode('utf-8'))
        self.assertEqual(3, len(content['objects']))
        slugs = [a['slug'] for a in content['objects']]
        self.assertEqual([
            'department-of-commerce',
            'department-of-homeland-security',
            'us-patent-and-trademark-office'],
            slugs)

    @skipIf(custom_backend == 'postgresql_psycopg2',
            'Test query in case postgres fails')
    def test_list_query_sqlite3(self):
        c = Client()
        response = c.get('/api/agency/?query=industry')
        self.assertEqual(200, response.status_code)
        content = helpers.json_from(response)
        self.assertEqual(len(content['objects']), 1)
        self.assertEqual(
            content['objects'][0]['slug'], 'department-of-commerce')

    @skipUnless(custom_backend == 'postgresql_psycopg2',
                'Only postgres has tsearch2')
    def test_list_query_postgres(self):
        """ Test that search works when backend is postgresql_psycopg2 """

        c = Client()
        response = c.get('/api/agency/?query=emergency')
        self.assertEqual(200, response.status_code)
        content = helpers.json_from(response)
        self.assertEqual(len(content['objects']), 1)
        self.assertEqual(
            content['objects'][0]['slug'],
            'department-of-homeland-security')

    @skipUnless(custom_backend == 'postgresql_psycopg2',
                'Only postgres has tsearch2')
    def test_list_query_order_and_fields(self):
        """
        Test that non-exact queries work and with multiple fields.
        """

        c = Client()
        # Test that search works with words not in order in title
        response = c.get('/api/agency/?query=cybersecurity+chemical')
        content = helpers.json_from(response)
        self.assertEqual(len(content['objects']), 1)
        self.assertEqual(
            content['objects'][0]['slug'],
            'department-of-homeland-security')

        # Test that search works with words not in order in description
        response = c.get('/api/agency/?query=Security+Homeland')
        content = helpers.json_from(response)
        self.assertEqual(len(content['objects']), 1)
        self.assertEqual(
            content['objects'][0]['slug'],
            'department-of-homeland-security')

        # Test that search works with abbeviations
        response = c.get('/api/agency/?query=dhs')
        content = helpers.json_from(response)
        self.assertEqual(len(content['objects']), 1)
        self.assertEqual(
            content['objects'][0]['slug'],
            'department-of-homeland-security')

        # Test that search works with slugs
        response = c.get(
            '/api/agency/?query=department-of-homeland-security')
        content = helpers.json_from(response)
        self.assertEqual(len(content['objects']), 1)
        self.assertEqual(
            content['objects'][0]['slug'],
            'department-of-homeland-security')

        # Test that search works with keywords
        response = c.get(
            '/api/agency/?query=forests')
        content = helpers.json_from(response)
        self.assertEqual(len(content['objects']), 1)
        self.assertEqual(
            content['objects'][0]['slug'],
            'department-of-commerce')

    @skipUnless(custom_backend == 'postgresql_psycopg2',
                'Only postgres has tsearch2')
    def test_list_query_quotes_errors(self):
        """
        Test quotes don't break the search.
        """
        c = Client()
        # single single quotes don't break search
        response = c.get("/api/agency/?query='test")
        self.assertEqual(response.status_code, 200)
        response = c.get("/api/agency/?query=te'st")
        self.assertEqual(response.status_code, 200)
        response = c.get("/api/agency/?query=test'")
        self.assertEqual(response.status_code, 200)
        response = c.get("/api/agency/?query='tes't test'")
        self.assertEqual(response.status_code, 200)

        # single double quotes don't break search
        response = c.get('/api/agency/?query="test')
        self.assertEqual(response.status_code, 200)
        response = c.get('/api/agency/?query=te"st')
        self.assertEqual(response.status_code, 200)
        response = c.get('/api/agency/?query=test"')
        self.assertEqual(response.status_code, 200)
        response = c.get('/api/agency/?query="tes"t test"')
        self.assertEqual(response.status_code, 200)

    @skipUnless(custom_backend == 'postgresql_psycopg2',
                'Only postgres has tsearch2')
    def test_list_query_and_or(self):
        """
        Test that or and and work correctly
        """

        # Using `AND` returns objects that contain both words
        c = Client()
        response = c.get('/api/agency/?query=vital+AND+homeland')
        content = helpers.json_from(response)
        self.assertEqual(len(content['objects']), 1)
        self.assertEqual(
            content['objects'][0]['slug'],
            'department-of-homeland-security')

        # Using `OR` returns objects that contain at least one of the words
        c = Client()
        response = c.get('/api/agency/?query=patents+OR+technological')
        content = helpers.json_from(response)
        self.assertEqual(len(content['objects']), 2)

    @skipUnless(custom_backend == 'postgresql_psycopg2',
                'Only postgres has tsearch2')
    def test_list_query_weighting(self):
        """
        Test that search returns results with query in title first rather
        than alphabetically
        """
        c = Client()
        response = c.get('/api/agency/?query=trademark')
        content = helpers.json_from(response)

        # Any results with `trademark` are returned
        self.assertEqual(len(content['objects']), 3)
        # But results with `trademark` in name are first
        self.assertEqual(
            content['objects'][0]['slug'],
            'us-patent-and-trademark-office')
        # And results with `trademark` in the keywords returned last
        self.assertEqual(
            content['objects'][2]['slug'],
            'department-of-homeland-security')

    def test_dictfetchall(self):
        """ Test that the raw sql converter works """

        cursor = connection.cursor()
        cursor.execute("select * from foia_hub_agency;")
        data = dictfetchall(cursor)
        self.assertEqual(len(data), 3)

        # Lists rendered as strings in DB are brought back as lists
        self.assertEqual(
            data[1].get('keywords'),
            ['business', 'industry', 'forests', 'petroleum'])

    def test_sanitize_search_term(self):
        """
        Test that raw strings are cleaned correctly to be used by to_tsquery
        """

        # Single words are turned into ingestible string
        test_term = sanitize_search_term('health')
        self.assertEqual(test_term, 'health:*')

        # Unspecified words connected with &
        test_term = sanitize_search_term('health justice')
        self.assertEqual(test_term, 'health:* & justice:*')

        # Single punctuation doesn't stay except for '&', '|', '-'
        test_term = sanitize_search_term("'he??alth justice")
        self.assertEqual(test_term, "health:* & justice:*")

        test_term = sanitize_search_term('health just#ice"')
        self.assertEqual(test_term, "health:* & justice:*")

        test_term = sanitize_search_term('health-justice"')
        self.assertEqual(test_term, "health-justice:*")

        test_term = sanitize_search_term('health & justice"')
        self.assertEqual(test_term, "health:* & justice:*")

        test_term = sanitize_search_term('health | justice"')
        self.assertEqual(test_term, "health:* | justice:*")

        test_term = sanitize_search_term('health|justice"')
        self.assertEqual(test_term, "health:*|justice:*")

        # Ands and Ors are converted
        test_term = sanitize_search_term('health AND justice')
        self.assertEqual(test_term, 'health:* & justice:*')
        test_term = sanitize_search_term('health OR justice')
        self.assertEqual(test_term, 'health:* | justice:*')

        # Complex search remains intact, but without punctuation
        test_term = sanitize_search_term(
            '"health life" AND justice OR "Justice AND Peace"')
        self.assertEqual(
            test_term,
            "health:* & life:* & justice:* | Justice:* & Peace:*")

    def test_detail(self):
        """ Check the detail view for an agency."""

        c = Client()
        response = c.get('/api/agency/department-of-homeland-security/')
        self.assertEqual(200, response.status_code)
        content = response.content
        content = json.loads(content.decode('utf-8'))
        self.assertEqual(content['name'], 'Department of Homeland Security')
        self.assertEqual(1, len(content['offices']))
        slug = 'department-of-homeland-security'
        slug += '--federal-emergency-management-agency'
        self.assertEqual(slug, content['offices'][0]['slug'])
        # test Stats models for both numbers and nulls
        self.assertEqual(37.5, content['complex_processing_time'])
        self.assertEqual(None, content['simple_processing_time'])

    def test_detail_components(self):
        """ Ensure the detail view for an agency includes the components. """

        c = Client()
        response = c.get('/api/agency/department-of-commerce/')
        self.assertEqual(200, response.status_code)
        content = helpers.json_from(response)
        self.assertEqual(content['name'], 'Department of Commerce')
        self.assertEqual(2, len(content['offices']))
        self.assertEqual(
            content['offices'][0]['slug'],
            'department-of-commerce--census-bureau')
        self.assertEqual(
            content['offices'][1]['slug'],
            'us-patent-and-trademark-office')

    def test_reading_rooms(self):
        c = Client()
        response = c.get('/api/agency/department-of-commerce/')
        self.assertEqual(200, response.status_code)
        content = helpers.json_from(response)
        self.assertEqual([{
            'link_text': 'The Electronic Reading Room',
            'url': 'http://www.doc.gov/err/'}],
            content['foia_libraries'])


class OfficeAPITests(TestCase):
    fixtures = [
        'agencies_test.json', 'offices_test.json', 'stats_test.json']

    def test_detail(self):
        """ Check the detail view for an agency."""

        c = Client()
        response = c.get('/api/office/department-of-commerce--census-bureau/')
        self.assertEqual(200, response.status_code)
        content = response.content
        content = json.loads(content.decode('utf-8'))
        self.assertEqual(content['name'], 'Census Bureau')
        self.assertEqual(
            'department-of-commerce--census-bureau',
            content['slug'])
        self.assertEqual(
            'department-of-commerce',
            content['agency_slug'])
        # test Stats models for both numbers and nulls
        self.assertEqual(12.2, content['complex_processing_time'])
        self.assertEqual(None, content['simple_processing_time'])

    def test_reading_room(self):
        """ Check that the detail view for an agency has the reading room
        links"""
        c = Client()
        slug = 'department-of-homeland-security'
        slug += '--federal-emergency-management-agency/'
        response = c.get('/api/office/%s' % slug)
        self.assertEqual(200, response.status_code)
        content = helpers.json_from(response)
        self.assertEqual([{
            'link_text': 'The Electronic Reading Room',
            'url': 'http://www.usmint.gov/FOIA/?action=room'}],
            content['foia_libraries'])
