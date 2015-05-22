import json
import time

from contact_updater.forms import AgencyForm

from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.http import HttpResponse

from foia_hub.api import AgencyResource, OfficeResource
from foia_hub.models import Agency


def form_index(request):
    """
    This function renders the landing page of the contact updater, which
    contains a links to each agencies update form.
    """
    agencies = Agency.objects.filter(parent__isnull=True).values()
    return render(
        request, "form_index.html", {'agencies': agencies})


def download_data(request):
    """ Converts POST request into JSON file ready for download """

    data = dict(request.POST)
    data['timestamp'] = int(time.time())
    del data['csrfmiddlewaretoken']
    res = HttpResponse(json.dumps(data), content_type="application/javascript")
    res['Content-Disposition'] = 'attachment; filename=contact_data.json'
    return res


def unpack_libraries(libraries):
    """ Given a list of libraries returns url """
    if libraries:
        return libraries[0].get('url')
    else:
        return ''


def join_array(array):
    """ Joins array feilds using `\n` """
    if array:
        return "\n".join(array)


def prepare_address_lines(lines):
    """ Splits address lines into two lines for form """
    data = {}
    if len(lines) > 0:
        data['address_line_1'] = lines[0]
    if len(lines) > 1:
        data['address_line_2'] = " ".join(lines[1:])
    return data


def prepare_emails(emails):
    """ Returns only the first email, else returns a blank line """
    data = {'emails': ''}
    if emails:
        data['emails'] = emails[0]
    return data


def transform_data(data):
    """ Returns only first email """
    data['foia_libraries'] = unpack_libraries(data.get('foia_libraries'))
    data['common_requests'] = join_array(data.get('common_requests'))
    data['no_records_about'] = join_array(data.get('no_records_about'))
    data.update(prepare_address_lines(data.get('address_lines')))
    data.update(prepare_emails(data.get('emails')))
    return data


def get_agency_data(slug):
    """
    Given an agency slug parse through the agency API and collect agency
    info to populate agency form. """
    agency_resource = AgencyResource()
    agency_data = [transform_data(agency_resource.detail(slug).value)]
    if agency_data[0].get('offices'):
        office_resource = OfficeResource()
        for office in agency_data[0].get('offices'):
            if '--' in office.get('slug'):
                office_data = office_resource.detail(office['slug']).value
            else:
                office_data = agency_resource.detail(office['slug']).value
            agency_data.append(transform_data(office_data))
    return agency_data


def prepopulate_agency(request, slug):
    """
    If GET request Collects agency and office data from foia_hub to
    populate the form. If POST request responds an attachment
    """
    return_data = {}

    agency_data = get_agency_data(slug=slug)
    agency_form_set = formset_factory(AgencyForm)

    if request.method == 'POST':
        formset = agency_form_set(request.POST)
        if formset.is_valid():
            return_data['validated'] = True
            if request.POST.get('download'):
                return download_data(request=request)
            elif request.POST.get('return'):
                return_data['validated'] = False
    else:
        formset = agency_form_set(initial=agency_data)

    management_form = formset.management_form
    return_data.update(
        {
            'agency_names': [item.get('name') for item in agency_data],
            'forms': formset[:-1],
            'management_form': management_form,
        })
    return render(request, "agency_form.html", return_data)
