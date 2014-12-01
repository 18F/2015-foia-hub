from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from jinja2 import Environment, PackageLoader

from foia_hub.models import Agency, FOIARequest
from foia_hub.api import AgencyResource, OfficeResource


env = Environment(loader=PackageLoader('foia_hub', 'templates'))
env.globals['ANALYTICS_ID'] = settings.ANALYTICS_ID

###
# Principal landing page for agencies and offices.
###


def contact_landing(request, slug):
    """List contacts for an agency or office."""
    if '--' in slug:
        resource = OfficeResource()
    else:
        resource = AgencyResource()

    data = resource.detail(slug).value

    if (data['is_a'] == 'agency') and (len(data.get("offices", [])) > 0):
        template = env.get_template('contacts/parent_profile.html')
    else:
        template = env.get_template('contacts/profile.html')
    return HttpResponse(template.render(
        profile=data, slug=slug, show_webform=settings.SHOW_WEBFORM))


###
# API endpoints
###

def get_agency_list():
    resource = AgencyResource()
    agencies = resource.list()
    agency_list = [
        {'name': agency.name, 'slug': agency.slug} for agency in agencies]
    return agency_list


###
# Flat pages
###

def learn(request):
    return HttpResponse(env.get_template('learn.html').render(request=request))


def about(request):
    return HttpResponse(env.get_template('about.html').render(request=request))

###
# Webform for agencies/offices that lack one of their own.
###


def request_form(request, slug=None):
    """Request form for an agency or office."""
    if '--' in slug:
        resource = OfficeResource()
    else:
        resource = AgencyResource()

    data = resource.detail(slug).value
    template = env.get_template('request/form.html')
    return HttpResponse(template.render(profile=data, slug=slug))


def request_success(request, id):
    #   @todo: this makes it easy for an attacker to harvest email addresses
    #   -- just look at all of the /success/##s in sequential order
    foia_request = get_object_or_404(FOIARequest, pk=id)
    requester = foia_request.requester
    office = foia_request.office
    agency = foia_request.agency or office.agency

    template = env.get_template('request/success.html')
    return HttpResponse(template.render(
        foia_request=foia_request, requester=requester, office=office,
        agency=agency))


def request_start(request):
    """ Starting a request. """
    agency_list = get_agency_list()
    most_requested_slugs = [
        'department-of-homeland-security',
        'department-of-justice',
        'department-of-defense',
        'department-of-health-and-human-services',
        'social-security-administration'
    ]
    most_requested = Agency.objects.filter(slug__in=most_requested_slugs)

    template = env.get_template('request/index.html')
    return HttpResponse(template.render(
        agencies=agency_list, most_requested=most_requested))
