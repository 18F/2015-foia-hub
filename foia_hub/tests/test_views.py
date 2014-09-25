from datetime import date

from django.core.urlresolvers import reverse
from django.test import SimpleTestCase
from mock import patch

from foia_hub.models import Agency, FOIARequest, Office, Requester


class RequestFormTests(SimpleTestCase):
    def setUp(self):
        self.agency = Agency(name='My Agency')
        self.agency.save()
        self.office = Office(agency=self.agency, name='An Office')
        self.office.save()
        self.office2 = Office(agency=self.agency, name='Other Office')
        self.office2.save()
        self.requester = Requester.objects.create(
            first_name='Alice', last_name='Bobson', email='eve@example.com')
        self.request = FOIARequest.objects.create(
            requester=self.requester, office=self.office,
            date_end=date.today(), request_body='All the cheese')

    def tearDown(self):
        self.request.delete()
        self.requester.delete()
        self.office2.delete()
        self.office.delete()
        self.agency.delete()

    def test_request_form_successful(self):
        """The agency name should be present in the request form"""
        response = self.client.get(reverse(
            'form', kwargs={'slug': self.agency.slug}))
        self.assertContains(response, "My Agency")

    def test_request_form_404(self):
        """Should get a 404 if requesting an agency that doesn't exist"""
        response = self.client.get(reverse(
            'form', kwargs={'slug': 'does-not-exist'}))
        self.assertEqual(404, response.status_code)

    def test_request_success(self):
        """Request should be retrieved and displayed"""
        response = self.client.get(reverse(
            'success', kwargs={'id': self.request.id}))
        self.assertContains(response, "eve@example.com")
        self.assertContains(response, "My Agency")

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
        response = self.client.get(reverse(
            'contact_landing', kwargs={'slug': 'sss--ss'}))
        self.assertEqual(response.status_code, 404)

    def test_contact_landing_success(self):
        """If loading an agency or a top-level office, we should see agency
        name. If an office, we should not see peer offices."""
        response = self.client.get(reverse(
            'contact_landing', kwargs={'slug': self.agency.slug}))
        self.assertContains(response, self.agency.name)
        self.assertContains(response, self.office.name)
        self.assertContains(response, self.office2.name)

        slug = self.agency.slug + '--' + self.office.slug
        response = self.client.get(reverse(
            'contact_landing', kwargs={'slug': slug}))
        self.assertContains(response, self.agency.name)
        self.assertContains(response, self.office.name)
        self.assertNotContains(response, self.office2.name)
