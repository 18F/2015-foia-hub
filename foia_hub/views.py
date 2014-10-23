from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from jinja2 import Environment, PackageLoader

from foia_hub.models import Agency, FOIARequest
from foia_hub.api import AgencyResource, OfficeResource


env = Environment(loader=PackageLoader('foia_hub', 'templates'))
env.globals['ANALYTICS_ID'] = settings.ANALYTICS_ID


def request_form(request, slug=None):
    agency = get_object_or_404(Agency, slug=slug)
    office = agency.office_set.first()

    template = env.get_template('request/form.html')
    return HttpResponse(template.render(agency=agency, office=office))

def get_agency_list():
    resource = AgencyResource()
    agencies = resource.list()
    agency_list = [
        {'name': agency.name, 'slug': agency.slug} for agency in agencies]
    return agency_list

def request_start(request):
    agency_list = get_agency_list()
    template = env.get_template('request/index.html')
    return HttpResponse(template.render(agencies=agency_list))


def learn(request):
    return HttpResponse(env.get_template('learn.html').render())


def request_success(request, id):
    #   @todo: this makes it easy for an attacker to harvest email addresses
    #   -- just look at all of the /success/##s in sequential order
    foia_request = get_object_or_404(FOIARequest, pk=id)
    requester = foia_request.requester
    office = foia_request.office
    agency = office.agency

    template = env.get_template('request/success.html')
    return HttpResponse(template.render(
        foia_request=foia_request, requester=requester, office=office,
        agency=agency))


def contact_landing(request, slug):
    """List contacts for an agency or office."""
    if '--' in slug:
        # -- indicates office.
        resource = OfficeResource()
    else:
        resource = AgencyResource()

    data = resource.detail(slug).value
    template = env.get_template('contacts/profile.html')
    return HttpResponse(template.render(profile=data))
