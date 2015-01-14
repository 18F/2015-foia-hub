from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from jinja2 import Environment, PackageLoader
from urllib.parse import urlparse

from foia_hub.models import FOIARequest
from foia_hub.api import AgencyResource, OfficeResource


env = Environment(loader=PackageLoader('foia_hub', 'templates'))
env.globals['ANALYTICS_ID'] = settings.ANALYTICS_ID

###
# Finding agencies and their contact information.
###


def home(request):
    """App home page."""
    return render(request, 'index.html', {})


def agencies(request):
    """Full agency listing."""
    query = request.GET.get("query")

    agencies = AgencyResource().list(query)
    if len(agencies) == 1:
        return redirect('contact_landing', slug=agencies[0].slug)
    else:
        return HttpResponse(env.get_template('contacts/index.html').render(
            agencies=agencies, query=query))


def contact_landing(request, slug):
    """Principal landing page for agencies and offices."""
    if '--' in slug:
        resource = OfficeResource()
    else:
        resource = AgencyResource()

    data = resource.detail(slug).value

    if (data['is_a'] == 'agency') and (len(data.get("offices", [])) > 0):
        return render(
            request,
            'contacts/parent_profile.html',
            {
                'profile': data,
                'slug': slug,
                'show_webform': settings.SHOW_WEBFORM
             })
    else:
        return render(
            request,
            'contacts/profile.html', 
            {
                'profile': data,
                'slug': slug,
                'show_webform': settings.SHOW_WEBFORM
            })


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
    return render(request, 'learn.html', {'request': request})


def about(request):
    return render(request, 'about.html', {'request': request})


def developers(request):
    return render(request, 'developers.html', {'request': request})

###
# Contacting agencies/offices that lack a webform of their own.
###


def request_form(request, slug=None):
    """Request form for an agency or office."""
    if '--' in slug:
        resource = OfficeResource()
    else:
        resource = AgencyResource()

    data = resource.detail(slug).value
    template = env.get_template('request/form.html')
    return render(
        request,
        'request/form.html',
        {'profile': data, 'slug': slug})


def request_noop(request):
    """ We have a request form that does nothing. Let's ensure the user knows
    that in the slim chance the form gets turned on in an environment it
    shouldn't be on in. """
    return render(request, 'request/noop.html', {})
