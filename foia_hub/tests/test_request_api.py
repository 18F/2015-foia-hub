import json
from django.test import TestCase, Client

from foia_hub.models import Agency


class FOIARequestTests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json']

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
