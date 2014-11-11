import json
from datetime import date

from django.core.urlresolvers import reverse
from django.test import SimpleTestCase, TestCase, Client
from mock import patch

from foia_hub.models import Agency, FOIARequest, Office, Requester
from foia_hub.views import get_agency_list
from foia_hub.tests import helpers

class RequestFormTests(SimpleTestCase):
    def setUp(self):
        self.emails = ["foia1@example.com", "foia2@example.com"]

        self.agency = Agency(name='Agency With Offices', zip_code=20404, emails=self.emails)
        self.agency.save()

        self.office = Office(
            agency=self.agency, name='Office 1', zip_code=20404, emails=self.emails)
        self.office.save()

        self.office2 = Office(
            agency=self.agency, name='Office 2', zip_code=20404, emails=self.emails)
        self.office2.save()

        self.agency2 = Agency(name='Agency Without Offices', zip_code=20009, emails=self.emails)

        self.requester = Requester.objects.create(
            first_name='Alice', last_name='Bobson', email='eve@example.com')
        self.request = FOIARequest.objects.create(
            requester=self.requester, office=self.office,
            date_end=date.today(), request_body='All the cheese')

    # destroy them all
    def tearDown(self):
        for model in [FOIARequest, Requester, Office, Agency]:
            model.objects.all().delete()

    def test_submit_request_to_agency(self):
        requester_email = "requester@example.com"
        self.assertEqual(0, len(Requester.objects.filter(email=requester_email)))

        response = self.client.post("/api/request/",
            content_type='application/json',
            data=json.dumps({
                'agency': self.agency.slug,

                'email': requester_email,
                'first_name': "FOIA",
                'last_name': "Requester",

                'body': "A new request",
            })
        )

        if response.status_code == 500:
            print(response.content)

        self.assertEqual(201, response.status_code)
        data = helpers.json_from(response)
        self.assertTrue(data.get('tracking_id') is not None)
        self.assertEqual('O', data.get('status'))

        request_id = data['tracking_id']
        foia_request = FOIARequest.objects.get(pk=request_id)
        self.assertTrue(foia_request is not None)
        self.assertEqual(1, len(Requester.objects.filter(email=requester_email)))
        self.assertEqual(requester_email, foia_request.requester.email)



    # def test_submit_request_to_office(self):
    #     pass

    # def test_submit_request_to_agency_with_more_data(self):
    #     response = self.client.post("/api/request/", {
    #         'agency': self.agency.slug,
    #         'body': "A new request",

    #         'documents_start': "November 11, 2014",
    #         'documents_end': "November 21, 2014",

    #         'email': "requester@example.com",
    #         'fee_limit': 2,
    #         'first_name': "FOIA",
    #         'last_name': "Requester",
    #     })

    def test_request_form_successful(self):
        """The agency name should be present in the request form"""
        response = self.client.get(reverse(
            'form', kwargs={'slug': self.agency.slug}))
        self.assertContains(response, self.agency.name)

    def test_request_form_404(self):
        """Should get a 404 if requesting an agency that doesn't exist"""
        response = self.client.get(reverse(
            'form', kwargs={'slug': 'does-not-exist'}))
        self.assertEqual(404, response.status_code)

    def test_request_success(self):
        """Request should be retrieved and displayed"""
        response = self.client.get(reverse(
            'success', kwargs={'id': self.request.id}))
        self.assertContains(response, self.requester.email)
        self.assertContains(response, self.agency.name)

    def test_request_success_404(self):
        """Should get a 404 if trying to get a success page for a request
        which doesn't exist"""
        response = self.client.get(reverse(
            'success', kwargs={'id': 9999999999}))
        self.assertEqual(404, response.status_code)

    @patch.dict('foia_hub.views.env.globals',
                {'ANALYTICS_ID': 'MyAwesomeAnalyticsCode'})
    def test_analytics_id(self):
        """Verify that the analytics id appears *somewhere* on the page"""
        response = self.client.get(reverse('request'))
        self.assertContains(response, 'MyAwesomeAnalyticsCode')

    def test_contact_landing_404(self):
        """Verify that non-existing agency/offices cause 404s"""
        response = self.client.get(reverse(
            'contact_landing', kwargs={'slug': 'sssss'}))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse('contact_landing', kwargs={'slug': 'sss--ss'}))
        self.assertEqual(response.status_code, 404)

    def test_contact_landing_success(self):
        """If loading an agency or a top-level office, we should see agency
        name. If an office, we should not see peer offices."""
        response = self.client.get(reverse(
            'contact_landing', kwargs={'slug': self.agency.slug}))
        self.assertContains(response, self.agency.name)
        self.assertContains(response, self.office.name)
        self.assertContains(response, self.office2.name)

        slug = self.office.slug
        response = self.client.get(reverse(
            'contact_landing', kwargs={'slug': slug}))
        self.assertContains(response, self.agency.name)
        self.assertContains(response, self.office.name)
        self.assertNotContains(response, self.office2.name)

    def test_learn(self):
        """The /learn/ page should load without errors."""
        response = self.client.get(reverse('learn'))
        self.assertEqual(response.status_code, 200)

class MainPageTests(TestCase):
    fixtures = ['agencies_test.json']

    def test_main_page(self):
        """ The main page should load without errors. """
        response = self.client.get(reverse('request'))
        self.assertEqual(response.status_code, 200)

    def test_get_agency_list(self):
        agencies = get_agency_list()
        self.assertEqual(agencies,
            [{
                'name': 'Department of Commerce',
                'slug': 'department-of-commerce'},
             {
                'name': 'Department of Homeland Security',
                'slug': 'department-of-homeland-security'}])

    def test_main_page_most_requested(self):
        response = self.client.get(reverse('request'))
        content = response.content.decode('utf-8')
        self.assertTrue('Most requests received' in content)

    def test_main_page_browse_all(self):
        response = self.client.get(reverse('request'))
        content = response.content.decode('utf-8')
        self.assertTrue('Browse all agencies' in content)
        self.assertTrue('Department of Commerce' in content)
        self.assertTrue('Department of Homeland Security' in content)

class ContactPageTests(TestCase):
    fixtures = ['agencies_test.json']

    def test_inaccurate_contact(self):
        response = self.client.get(
            reverse('contact_landing',
            args=['department-of-homeland-security']))
        self.assertTrue(200, response.status_code)
        content = response.content.decode('utf-8')
        self.assertTrue('Contact us so we can fix it' in content)
        self.assertTrue('18f-foia@gsa.gov' in content)
