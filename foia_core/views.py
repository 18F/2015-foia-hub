import json


from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict

from foia_core.models import *



def agency_data(request):

    data = serializers.serialize('json', Agency.objects.all(), indent=4)
    return HttpResponse(data, content_type="application/json")

    # Django 1.7 will have JsonResponse, which is a subclass of HttpResponse
    # but JSON-encoded.
    # return JsonResponse({"key": "value"})

def office_data(request, slug):

    offices = Office.objects.filter(agency__slug=slug)
    data = serializers.serialize('json', offices, indent=4)
    return HttpResponse(data, content_type="application/json")
