import json
import sys
from django.test import TestCase, Client
from django.conf import settings
from imp import reload
from importlib import import_module

from foia_hub.models import Agency, Office, Requester, FOIARequest
from foia_hub.tests import helpers


class FOIARequestTests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json']

    def setUp(self):
        self.emails = ["foia1@example.com", "foia2@example.com"]
        self.agency = Agency(
            name='Agency With Offices', zip_code=20404, emails=self.emails)
        self.agency.save()
        self.office = Office(
            agency=self.agency, name='Office 1', zip_code=20404,
            emails=self.emails)
        self.office.save()

    def test_create_request(self):
        """ Submit a simple, minimal FOIA request to the API and expect it to
        succeed.  """

        c = Client()

        data = {
            'agency': 'department-of-commerce',
            'first_name': 'Joe',
            'last_name': 'Public',
            'email': 'joe@public.com',
            'body': 'I want documents about palm trees.'
        }

        data_string = json.dumps(data)
        response = c.post(
            '/api/request/', content_type="application/json", data=data_string)
        self.assertEqual(201, response.status_code)

    def test_create_request_no_email(self):
        """ Try to submit a request to an agency that has no online form, and
        no email address. This should fail with the appropriate HTTP status
        code. """

        a = Agency(name="Broadcasting Board of Governors", slug="broadcasting")
        a.save()

        c = Client()

        data = {
            'agency': 'broadcasting',
            'first_name': 'Joe',
            'last_name': 'Public',
            'email': 'joe@public.com',
            'body': 'I want documents about palm trees.'
        }
        data_string = json.dumps(data)
        response = c.post(
            '/api/request/', content_type="application.json", data=data_string)
        self.assertEqual(400, response.status_code)

    def test_submit_request_to_agency(self):
        requester_email = "requester@example.com"
        self.assertEqual(
            0, len(Requester.objects.filter(email=requester_email)))

        response = self.client.post(
            "/api/request/",
            content_type='application/json',
            data=json.dumps({
                'agency': self.agency.slug,

                'email': requester_email,
                'first_name': "FOIA",
                'last_name': "Requester",

                'body': "A new request",
            })
        )

        self.assertEqual(201, response.status_code, response.content)
        data = helpers.json_from(response)
        self.assertTrue(data.get('tracking_id') is not None)
        self.assertEqual('O', data.get('status'))

        request_id = data['tracking_id']
        foia_request = FOIARequest.objects.get(pk=request_id)
        self.assertTrue(foia_request is not None)
        self.assertEqual(foia_request.agency, self.agency)
        self.assertEqual(
            1, len(Requester.objects.filter(email=requester_email)))
        self.assertEqual(requester_email, foia_request.requester.email)

    def test_submit_request_to_office(self):
        requester_email = "requester@example.com"
        self.assertEqual(
            0, len(Requester.objects.filter(email=requester_email)))

        response = self.client.post(
            "/api/request/",
            content_type='application/json',
            data=json.dumps({
                'agency': self.office.agency.slug,
                'office': self.office.office_slug,

                'email': requester_email,
                'first_name': "FOIA",
                'last_name': "Requester",

                'body': "A new request",
            })
        )

        self.assertEqual(201, response.status_code, response.content)
        data = helpers.json_from(response)
        self.assertTrue(data.get('tracking_id') is not None)
        self.assertEqual('O', data.get('status'))

        request_id = data['tracking_id']
        foia_request = FOIARequest.objects.get(pk=request_id)
        self.assertTrue(foia_request is not None)
        self.assertEqual(foia_request.office, self.office)
        self.assertEqual(
            1, len(Requester.objects.filter(email=requester_email)))
        self.assertEqual(requester_email, foia_request.requester.email)

    def test_submit_invalid_request(self):
        requester_email = "requester@example.com"
        self.assertEqual(
            0, len(Requester.objects.filter(email=requester_email)))

        response = self.client.post(
            "/api/request/",
            content_type='application/json',
            data=json.dumps({
                'agency': "not-a-valid-agency",

                'email': requester_email,
                'first_name': "FOIA",
                'last_name': "Requester",

                'body': "A new request",
            })
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual(
            0, len(Requester.objects.filter(email=requester_email)))


class RequestSwitchTests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json']

    def reload_urls(self):
        """ The flag the turns of the requests API is in urls.py, so we have to
        reload the URLs in Django to make tests. This reloads those tests. """

        if settings.ROOT_URLCONF in sys.modules:
            reload(sys.modules[settings.ROOT_URLCONF])
            import_module(settings.ROOT_URLCONF)

    def setUp(self):
        self.emails = ["foia1@example.com", "foia2@example.com"]
        self.agency = Agency(
            name='Agency With Offices', zip_code=20404, emails=self.emails)
        self.agency.save()
        self.office = Office(
            agency=self.agency, name='Office 1', zip_code=20404,
            emails=self.emails)
        self.office.save()

        # Turn off SHOW_WEBFORM
        settings.SHOW_WEBFORM = False
        self.reload_urls()

    def tearDown(self):
        # Turn on SHOW_WEBFORM
        settings.SHOW_WEBFORM = True
        self.reload_urls()

    def test_api_off(self):
        """ The request API should not the available. """

        requester_email = "requester@example.com"
        response = self.client.post(
            "/api/request/",
            content_type='application/json',
            data=json.dumps({
                'agency': self.agency.slug,
                'email': requester_email,
                'first_name': "FOIA",
                'last_name': "Requester",
                'body': "A new request"}))
        self.assertEqual(404, response.status_code)
