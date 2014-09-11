from django.http import HttpResponse
import datetime

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('foia_hub', 'templates'))

import json
from django.core.serializers.json import DjangoJSONEncoder

from foia_hub.models import Agency, Office, FOIARequest

def request_form(request, slug=None):
    agency = Agency.objects.filter(slug=slug).first()
    office = agency.office_set.first()

    template = env.get_template('request/form.html')
    return HttpResponse(template.render(agency=agency, office=office))

def request_start(request):
    template = env.get_template('request/index.html')
    return HttpResponse(template.render())

def request_success(request, id):
    foia_request = FOIARequest.objects.filter(id=id).first()
    requester = foia_request.requester
    office = foia_request.office
    agency = office.agency

    template = env.get_template('request/success.html')
    return HttpResponse(template.render(foia_request=foia_request, requester=requester, office=office, agency=agency))

# similar to agency API, but optimized for typeahead consumption
def request_autocomplete(request):
    agencies = Agency.objects.order_by('name').all()
    response = []
    for agency in agencies:
        response.append({
            "name": agency.name,
            "description": agency.description,
            "abbreviation": agency.abbreviation,
            "slug": agency.slug,
            "keywords": agency.keywords
        })
    agency_json = json.dumps(response, cls=DjangoJSONEncoder)
    return HttpResponse(agency_json, content_type = "application/json")
