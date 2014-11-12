import datetime

from django.db import transaction
from django.conf.urls import patterns, url
from django.shortcuts import get_object_or_404

from restless.dj import DjangoResource
from restless.resources import skip_prepare
from restless.preparers import FieldsPreparer

from foia_hub.models import Agency, Office, Requester, Stats


def contact_preparer():
    return FieldsPreparer(fields={
        'name': 'name',
        'person_name': 'person_name',
        'emails': 'emails',
        'phone': 'phone',
        'toll_free_phone': 'toll_free_phone',
        'fax': 'fax',

        'public_liaison_name': 'public_liaison_name',
        'public_liaison_email': 'public_liaison_email',
        'public_liaison_phone': 'public_liaison_phone',

        'request_form_url': 'request_form_url',
        'office_url': 'office_url',

        'address_lines': 'address_lines',
        'street': 'street',
        'city': 'city',
        'state': 'state',
        'zip_code': 'zip_code'
        })


def agency_preparer():
    return FieldsPreparer(fields={
        'name': 'name',
        'description': 'description',
        'abbreviation': 'abbreviation',
        'slug': 'slug',
        'keywords': 'keywords',
        'common_requests': 'common_requests'
    })


def office_preparer():
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
        'slug': 'slug',
    })
    return preparer


class AgencyResource(DjangoResource):
    """ The resource that represents the endpoint for an Agency """

    preparer = agency_preparer()

    def __init__(self, *args, **kwargs):
        super(AgencyResource, self).__init__(*args, **kwargs)
        self.office_preparer = office_preparer()
        self.contact_preparer = contact_preparer()

    def prepare_agency_contact(self, agency):
        offices = []
        for o in agency.office_set.order_by('name').all():
            offices.append(self.office_preparer.prepare(o))

        data = {
            'offices': offices,
            'is_a': 'agency',
            'agency_slug': agency.slug,
            'agency_name': agency.name,
            "no_records_about": agency.no_records_about
        }
        data.update(AgencyResource.preparer.prepare(agency))
        data.update(self.contact_preparer.prepare(agency))
        return data

    def list(self):
        """ This lists all the Agency objects. It doesn't provide every field
        for every object, instead limiting the output to useful fields. To see
        the detail for each object, use the detail endpoint. """
        return Agency.objects.all().order_by('name')

    @skip_prepare
    def detail(self, slug):
        """ A detailed return of an Agency objects. """
        agency = get_object_or_404(Agency, slug=slug)
        response = self.prepare_agency_contact(agency)
        return response

    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(
            AgencyResource, cls).urls(name_prefix=name_prefix)
        return patterns(
            '',
            url(
                r'^(?P<slug>[\w-]+)/$',
                cls.as_view('detail'),
                name=cls.build_url_name('detail', name_prefix)),
            ) + urlpatterns


class OfficeResource(DjangoResource):
    """ The resource that represents the endpoint for an Office. """

    def __init__(self, *args, **kwargs):
        super(OfficeResource, self).__init__(*args, **kwargs)
        self.agency_preparer = agency_preparer()
        self.office_preparer = office_preparer()
        self.contact_preparer = contact_preparer()

    @skip_prepare
    def detail(self, slug):
        """ A detailed return of an Office object. """
        office = get_object_or_404(Office, slug=slug)
        response = self.prepare_office_contact(office)
        return response

    def prepare_office_contact(self, office):
        office_data = self.office_preparer.prepare(office)

        data = {
            'agency_name': office.agency.name,
            'agency_slug': office.agency.slug,
            'office_slug': office.office_slug,
            'agency_description': office.agency.description,
            'is_a': 'office'
        }

        data.update(office_data)
        data.update(self.contact_preparer.prepare(office))
        return data

    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(
            OfficeResource, cls).urls(name_prefix=name_prefix)
        return patterns(
            '',
            url(
                r'^(?P<slug>[\w-]+)/$',
                cls.as_view('detail'),
                name=cls.build_url_name('detail', name_prefix)),
            ) + urlpatterns


class FOIARequestResource(DjangoResource):

    preparer = FieldsPreparer(fields={
        'status': 'status',
        'tracking_id': 'pk',
    })

    def _convert_date(self, date):
        return datetime.datetime.strptime(date, '%B %d, %Y')

    # POST /
    def create(self):

        foia = None
        with transaction.atomic():

            # Is this request to an Agency, or an Office?
            if self.data.get('office') and self.data.get('agency'):
                office = Office.objects.get(
                    agency__slug=self.data['agency'],
                    office_slug=self.data['office'],
                )
                agency = None
                emails = office.emails
            elif self.data.get('agency'):
                agency = Agency.objects.get(
                    slug=self.data['agency']
                )
                office = None
                emails = agency.emails

            # Not sure yet what this actually returns.
            # restless docs could be better on this point.
            else:
                raise Exception("No agency or office given.")

            requester = Requester.objects.create(
                first_name=self.data['first_name'],
                last_name=self.data['last_name'],
                email=self.data['email']
            )

            if self.data.get("documents_start"):
                start = self._convert_date(self.data['documents_start'])
            else:
                start = None

            if self.data.get("documents_end"):
                end = self._convert_date(self.data['documents_end'])
            else:
                end = None

            foia = FOIARequest.objects.create(
                status='O',
                requester=requester,
                office=office,
                agency=agency,
                emails=emails,
                date_start=start,
                date_end=end,
                request_body=self.data['body'],
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


class StatsResource(DjangoResource):

    preparer = FieldsPreparer(fields={
        'agency': 'agency',
        'office': 'office',
        'year': 'year',
        'stat_type': 'stat_type',
        'average': 'average',
        'median': 'median',
        'high': 'high',
        'low': 'low',
    })

    def __init__(self, *args, **kwargs):
        super(StatsResource, self).__init__(*args, **kwargs)
        self.agency_preparer = agency_preparer()
        self.office_preparer = office_preparer()


    def prepare_stats_record(self,stat):
        '''prepares one record'''
        prepared_stat = self.preparer.prepare(stat)
        office = stat.office
        if office:
            office_name = office.slug
        else:
            office_name = None
        data = {
            'agency': stat.agency.slug,
            'office': office_name,
        }
        prepared_stat.update(data)
        return prepared_stat


    def prepare_stats_records(self, stats):
        '''prepares multiple records'''
        response = []
        for stat in stats:
            response.append(self.prepare_stats_record(stat))
        return response


    def get_agency_office(self, slug):
        '''returns agency and office from slug'''
        agency = Agency.objects.get(slug=slug.split("--")[0])
        if "--" in slug:
            office = Office.objects.get(slug=slug)
        else:
            office = None
        return agency, office

    def transform_stats_type(self,stat_type):
        '''converts readable stats type into database queries'''

        if "simple-requests" == stat_type:
            return "S"
        elif "complex-requests" == stat_type:
            return "C"
        elif "expedited-requests" == stat_type:
            return "E"
        else:
            return "error"

    @skip_prepare
    def list(self, slug = None, year = None, stat_type = None):
        '''prepares a list endpoint with optional args'''
        kwargs = {}
        if year:
            kwargs['year'] = year
        if stat_type:
            kwargs['stat_type'] = self.transform_stats_type(stat_type)
        if slug:
            kwargs['agency'], kwargs['office'] = self.get_agency_office(slug)
            stats = Stats.objects.filter(**kwargs)
            return self.prepare_stats_records(stats)
        else:
            return self.prepare_stats_records(Stats.objects.all())


    @classmethod
    def urls(cls, name_prefix=None):
        '''generate optional patterns for different endpoints'''
        urlpatterns = super(
            StatsResource, cls).urls(name_prefix=name_prefix)
        return patterns(
            '',
            url(
                r'^(?P<slug>[\w-]+)/$',
                cls.as_view('list'),
                name=cls.build_url_name('list', name_prefix)),
           url(
                r'^(?P<slug>[\w-]+)/(?P<year>[\d]+)/$',
                cls.as_view('list'),
                name=cls.build_url_name('list', name_prefix)),
            url(
                r'^(?P<slug>[\w-]+)/(?P<year>[\d]+)/(?P<stat_type>[\w-]+)/$',
                cls.as_view('list'),
                name=cls.build_url_name('list', name_prefix)),
            ) + urlpatterns


    def is_authenticated(self):
        return True

