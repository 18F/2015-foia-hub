import datetime

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from foia_core.models import *



class AgencyResource(DjangoResource):

    preparer = FieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
        'abbreviation': 'abbreviation',
        'description': 'description',
        'slug': 'slug',
    })

    # GET /
    def list(self):
        return Agency.objects.all()


class OfficeResource(DjangoResource):

    preparer = FieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
        'slug': 'slug',

        'service_center': 'service_center',
        'fax': 'fax',

        'request_form': 'request_form',
        'website': 'website',
        'emails': 'emails',

        'contact': 'contact',
        'contact_phone': 'contact_phone',
        'public_liaison': 'public_liaison',

        'notes': 'notes',
    })

    # GET /
    def list(self, slug):
        return Office.objects.filter(agency__slug=slug)


class FOIARequestResource(DjangoResource):

    preparer = FieldsPreparer(fields={
        'status': 'status',
        'requester': 'requester.pk',
        'date_start': 'date_start',
        'date_end': 'date_end',
        'fee_limit': 'fee_limit',
        'request_body': 'request_body',
        'custom_fields': 'custom_fields',
        #'agency': 'agency',
    })

    def _convert_date(self, date):
        return datetime.datetime.strptime(date, '%B %d, %Y')

    # POST /
    def create(self):

        import pprint
        pprint.pprint(self.data)

        office = Office.objects.get(
            agency__slug=self.data['agency'],
            slug=self.data['office'],
        )

        requester = Requester.objects.create(
            first_name=self.data['first_name'],
            last_name=self.data['last_name'],
            email=self.data['email']
        )

        start = self._convert_date(self.data['documents_start'])
        end = self._convert_date(self.data['documents_end'])

        return FOIARequest.objects.create(
            status='O',
            requester = requester,
            office = office,
            date_start=start,
            date_end=end,
            request_body=self.data['body'],
            custom_fields=self.data['agency_fields'],
        )

    # GET /
    def list(self):
        return FOIARequest.objects.all()

    # Open everything wide!
    # DANGEROUS, DO NOT DO IN PRODUCTION.
    # more info here: https://github.com/toastdriven/restless/blob/master/docs/tutorial.rst
    def is_authenticated(self):
        return True
