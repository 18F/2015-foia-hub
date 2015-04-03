from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView

from foia_hub.api import AgencyResource, OfficeResource

###
# Custom TemplateView for adding small search
###


class SmallSearchView(TemplateView):

    def get_context_data(self, **kwargs):
            context = super(SmallSearchView, self).get_context_data(**kwargs)
            context['smallsearch'] = True
            return context


###
# Finding agencies and their contact information.
###


def agencies(request):
    """Full agency listing."""
    query = request.GET.get("query")

    agencies = AgencyResource().list(query)
    return render(
        request,
        'contacts/index.html',
        {
            'agencies': agencies,
            'query': query,
            'smallsearch': True
        })


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
                'show_webform': settings.SHOW_WEBFORM,
                'smallsearch': True
            })
    else:
        return render(
            request,
            'contacts/profile.html',
            {
                'profile': data,
                'slug': slug,
                'show_webform': settings.SHOW_WEBFORM,
                'smallsearch': True
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
# Contacting agencies/offices that lack a webform of their own.
###


def request_form(request, slug=None):
    """Request form for an agency or office."""
    if '--' in slug:
        resource = OfficeResource()
    else:
        resource = AgencyResource()

    data = resource.detail(slug).value
    return render(
        request,
        'request/form.html',
        {'profile': data, 'slug': slug})


def request_noop(request):
    """ We have a request form that does nothing. Let's ensure the user knows
    that in the slim chance the form gets turned on in an environment it
    shouldn't be on in. """
    return render(request, 'request/noop.html', {})
