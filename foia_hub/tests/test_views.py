from datetime import date

from django.test import SimpleTestCase

from foia_hub.models import Agency, FOIARequest, Office, Requester


class RequestFormTests(SimpleTestCase):
    def setUp(self):
        self.agency = Agency(name='My Agency')
        self.agency.save()
        self.office = Office(agency=self.agency, name='An Office')
        self.office.save()
        self.requester = Requester.objects.create(
            first_name='Alice', last_name='Bobson', email='eve@example.com')
        self.request = FOIARequest.objects.create(
            requester=self.requester, office=self.office,
            date_end=date.today(), request_body='All the cheese')

    def tearDown(self):
        self.request.delete()
        self.requester.delete()
        self.office.delete()
        self.agency.delete()

    def test_request_form_successful(self):
        """The agency name should be present in the request form"""
        response = self.client.get('/request/' + self.agency.slug + '/')
        self.assertContains(response, "My Agency")

    def test_request_form_404(self):
        """Should get a 404 if requesting an agency that doesn't exist"""
        response = self.client.get('/request/does-not-exist/')
        self.assertEqual(404, response.status_code)

    def test_request_success(self):
        """Request should be retrieved and displayed"""
        response = self.client.get('/request/success/'
                                   + str(self.request.id) + '/')
        self.assertContains(response, "eve@example.com")
        self.assertContains(response, "My Agency")

    def test_request_success_404(self):
        """Should get a 404 if trying to get a success page for a request
        which doesn't exist"""
        response = self.client.get('/request/success/999999999/')
        self.assertEqual(404, response.status_code)
