import datetime

from django.db import transaction
from django.conf.urls import patterns, url
from django.shortcuts import get_object_or_404

from restless.dj import DjangoResource
from restless.resources import skip_prepare
from restless.preparers import FieldsPreparer

from foia_hub.models import *


def agency_preparer():
    return FieldsPreparer(fields={
        'name': 'name',
        'description': 'description',
        'abbreviation': 'abbreviation',
        'slug': 'slug',
        'keywords': 'keywords'
    })


def office_preparer():
    return FieldsPreparer(fields={
        'name': 'name',
        'slug': 'slug'})


def full_office_preparer():
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
        'slug': 'slug',

        #'service_center': 'service_center',
        'fax': 'fax',

        #'request_form': 'request_form',
        #'website': 'website',
        #'emails': 'emails',

        #'contact': 'contact',
        #'contact_phone': 'contact_phone',
        #'public_liaison': 'public_liaison',

        #'notes': 'notes',
    })
    return preparer


class AgencyOfficeResource(DjangoResource):
    """ This helps implement endpoints for discoverable entities. Discoverable
    entities are Agencies and those Offices that are designated as top-tier.
    """

    def __init__(self, *args, **kwargs):
        super(AgencyOfficeResource, self).__init__(*args, **kwargs)
        self.http_methods.update({
            'autocomplete': {
                'GET': 'autocomplete',
            },
            'contact': {
                'GET': 'contact',
            }
        })

        self.agency_preparer = agency_preparer()
        self.office_preparer = office_preparer()
        self.full_office_preparer = full_office_preparer()

    @skip_prepare
    def autocomplete(self):
        agencies = Agency.objects.all()
        response = [self.agency_preparer.prepare(a) for a in agencies]
        response.sort(key=lambda x: x['name'])
        return response

    def prepare_office_contact(self, office):
        office_data = self.full_office_preparer.prepare(office)

        data = {
            'agency_name': office.agency.name,
            'agency_slug': office.agency.slug,
            'agency_description': office.agency.description,
            'offices': [office_data],
            'is_a': 'office'
        }
        return data

    def prepare_agency_contact(self, agency):
        offices = []
        for o in agency.office_set.all():
            offices.append(self.full_office_preparer.prepare(o))

        data = {
            'agency_name': agency.name,
            'agency_slug': agency.slug,
            'agency_description': agency.description,
            'offices': offices,
            'is_a': 'agency',
            "common_requests": agency.common_requests,
            "no_records_about": agency.no_records_about
        }
        return data

    @skip_prepare
    def contact(self, slug):
        if '--' in slug:
            # Searchable slugs are a compound of agency.slug and office.slug,
            # separated by a '---'. We split those out here for searching.
            #agency_slug, office_slug = slug.split('--')

            #office = get_object_or_404(
            #    Office, agency__slug=agency_slug, slug=office_slug)
            office = get_object_or_404(
                Office,
                slug=slug
            )
            agencyoffice = office
            response = self.prepare_office_contact(office)
        else:
            agency = get_object_or_404(Agency, slug=slug)
            agencyoffice = agency
            response = self.prepare_agency_contact(agency)

        response.update({
            'name': agencyoffice.name,
            'person_name': agencyoffice.person_name,
            'emails': agencyoffice.emails,
            'phone': agencyoffice.phone,
            'toll_free_phone': agencyoffice.toll_free_phone,
            'fax': agencyoffice.fax,

            'public_liaison_name': agencyoffice.public_liaison_name,
            'public_liaison_email': agencyoffice.public_liaison_email,
            'public_liaison_phone': agencyoffice.public_liaison_phone,

            'request_form_url': agencyoffice.request_form_url,
            'office_url': agencyoffice.office_url,

            'address_lines': agencyoffice.address_lines,
            'street': agencyoffice.street,
            'city': agencyoffice.city,
            'state': agencyoffice.state,
            'zip_code': agencyoffice.zip_code
        })

        return response

    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(
            AgencyOfficeResource, cls).urls(name_prefix=name_prefix)
        return urlpatterns + patterns(
            '',
            url(
                r'^autocomplete/$',
                cls.as_view('autocomplete'),
                name=cls.build_url_name('autocomplete', name_prefix)),
            url(
                r'^contact/(?P<slug>[\w-]+)/$',
                cls.as_view('contact'),
                name=cls.build_url_name('contact', name_prefix)),
            )


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
        return Agency.objects.order_by('name').all()


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
        'tracking_id': 'pk',
    })

    def _convert_date(self, date):
        return datetime.datetime.strptime(date, '%B %d, %Y')

    # POST /
    def create(self):

        foia = None
        with transaction.atomic():

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

            foia = FOIARequest.objects.create(
                status='O',
                requester=requester,
                office=office,
                date_start=start,
                date_end=end,
                request_body=self.data['body'],
                custom_fields=self.data['agency_fields'],
            )

        return foia

    # GET /
    def list(self):
        return FOIARequest.objects.all()

    # Open everything wide!
    # DANGEROUS, DO NOT DO IN PRODUCTION.
    # more info here:
    # https://github.com/toastdriven/restless/blob/master/docs/tutorial.rst
    def is_authenticated(self):
        return True
