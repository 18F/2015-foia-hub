import json
import time

from contact_updater.forms import AgencyData

from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.http import HttpResponse

from foia_hub.api import AgencyResource, OfficeResource


def form_index(request):
    agencies = AgencyResource().list()
    return render(
        request, "form_index.html", {'agencies': agencies})


def download_data(request, slug):
    """ Converts POST request into json file ready for download """

    data = dict(request.POST)
    data['timestamp'] = int(time.time())
    del data['csrfmiddlewaretoken']
    res = HttpResponse(json.dumps(data), content_type="application/javascript")
    res['Content-Disposition'] = 'attachment; filename=%s.json' % slug
    return res


def get_first_element(array):
    """ Given a list returns first element """

    if array:
        return array[0]


def unpack_libraries(libraries):
    """ Given a list of libraries returns url """

    if libraries:
        return libraries[0].get('url')


def join_array(array):
    """ Joins array feilds using `\n` """
    if array:
        return "\n".join(array)


def transform_data(data):
    """ Returns only first email """

    data['emails'] = get_first_element(data.get('emails'))
    data['foia_libraries'] = unpack_libraries(data.get('foia_libraries'))
    data['common_requests'] = join_array(data.get('common_requests'))
    data['no_records_about'] = join_array(data.get('no_records_about'))
    data['address_lines'] = join_array(data.get('address_lines'))
    return data


def get_agency_data(slug):
    """
    Given an agency slug parse through the agency API and collect agency
    info to populate agency form
    """
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
    agency_form_set = formset_factory(AgencyData)
    # I think we'll need a special endpoint for this
    # looping though multiple pages is taking too long
    agency_data = get_agency_data(slug=slug)
    if request.method == "GET":
        formset = agency_form_set(initial=agency_data)

    elif request.method == 'POST':
        formset = agency_form_set(request.POST)
        if formset.is_valid():
            return_data['validated'] = True
            if request.POST.get('download'):
                return download_data(request=request, slug=slug)
            elif request.POST.get('return'):
                return_data['validated'] = False

    management_form = formset.management_form
    return_data.update(
        {
            'data': zip(agency_data, formset),
            'management_form': management_form,
        })
    return render(request, "agency_form.html", return_data)
