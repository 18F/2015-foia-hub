import json


from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict

from foia_core.models import *



def agency_data(request):

    objectQuerySet = Agency.objects.select_related()
    data = serializers.serialize('json', objectQuerySet)

    return HttpResponse(data,
        content_type="application/json")

    # Django 1.7 will have JsonResponse, which is a subclass of HttpResponse
    # but JSON-encoded.
    # return JsonResponse({"key": "value"})
