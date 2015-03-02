#!/usr/bin/env python

import logging
import os
import string
import sys

import yaml
from glob import iglob
import django

from foia_hub.models import Agency, Office, Stats, ReadingRoomUrls

django.setup()
logger = logging.getLogger(__name__)


def check_urls(agency_url, row, field):
    # Because only some rows have websites, we only want to update if they do.
    row_url = row.get(field, None)
    # Check if the existing rec has a url & if it doesn't
    # match, then we end up with two conflicting records.
    # In this case, we need to reaccess website on agency.
    if agency_url and (agency_url != row_url):
        logger.warning('Two records with the same agency have two diff urls.')
        logger.warning('1:%s | 2:%s' % (agency_url, row_url))
        logger.warning('Website: %s, was not saved.' % (row_url))
        return agency_url
    else:
        return row_url


def extract_tty_phone(service_center):
    """ Extract a TTY phone number if one exists from the service_center
    entry in the YAML. """

    tty_phones = [p for p in service_center['phone'] if 'TTY' in p]
    if len(tty_phones) > 0:
        return tty_phones[0]


def extract_non_tty_phone(public_liaison):
    """ Extract a non-TTY number if one exists, otherwise use the TTY number.
    If there are multiple options, for now pick the first one. Return None if
    no phone number """

    if 'phone' in public_liaison:
        non_tty = [p for p in public_liaison['phone'] if 'TTY' not in p]
        if len(non_tty) > 0:
            return non_tty[0]
        elif len(public_liaison['phone']) > 0:
            return public_liaison['phone'][0]


def contactable_fields(agency, office_dict):
    """Add the Contactable and USAddress fields to the agency based on values
    in the office dictionary. This will be called for both parent and child
    agencies/offices (as written in our current data set)"""

    agency.phone = office_dict.get('phone')
    agency.emails = office_dict.get('emails', [])
    agency.fax = office_dict.get('fax')
    agency.office_url = office_dict.get('website')
    agency.request_form_url = office_dict.get('request_form')

    service_center = office_dict.get(
        'service_center', {'name': None, 'phone': ['']})
    agency.TTY_phone = extract_tty_phone(service_center)
    agency.person_name = service_center.get('name')

    public_liaison = office_dict.get(
        'public_liaison', {'name': None, 'phone': []})
    agency.public_liaison_phone = extract_non_tty_phone(public_liaison)
    agency.public_liaison_name = public_liaison.get('name')

    address = office_dict.get('address', )
    agency.zip_code = address.get('zip')
    agency.state = address.get('state')
    agency.city = address.get('city')
    agency.street = address.get('street')
    agency.address_lines = address.get('address_lines', [])
    update_reading_rooms(agency, office_dict)


def add_request_time_statistics(data, agency, office=None):
    """Load stats data about agencies into the database."""

    # Delete old stats before adding
    Stats.objects.filter(agency=agency, office=office).delete()

    if data.get('request_time_stats'):
        latest_year = sorted(
            data.get('request_time_stats').keys(), reverse=True)[0]
        data = data['request_time_stats'].get(latest_year)
        if data:
            iterator = [('S', 'simple'), ('C', 'complex')]
            for arg in iterator:
                median = data.get("%s_median_days" % arg[1])
                if median:
                    stat = Stats(
                        agency=agency,
                        office=office,
                        year=int(latest_year),
                        stat_type=arg[0])

                    if median == 'less than 1':
                        stat.median = 1
                        stat.less_than_one = True
                    else:
                        stat.median = median
                    stat.save()


def update_reading_rooms(contactable, data):
    """ This ensures that the reading rooms indicated in `data` are added to
    the contactable (agency, office). If the contactable already has reading
    rooms, those are deleted first. """

    # Delete all existing reading rooms, because we'll re-add them.
    contactable.reading_room_urls.all().delete()

    for link_text, url in data.get('reading_rooms', []):
        rru = ReadingRoomUrls(
            content_object=contactable, link_text=link_text, url=url)
        rru.save()


def build_abbreviation(agency_name):
    """ Given an agency name, guess at an abbrevation. """
    abbreviation = ''
    for ch in agency_name:
        if ch in string.ascii_uppercase:
            abbreviation += ch
    return abbreviation


def load_agency_fields(agency, data):
    """ Loads agency-specific values """

    abbreviation = data.get('abbreviation')
    if not abbreviation:
        abbreviation = build_abbreviation(data.get('name'))
    agency.abbreviation = abbreviation
    agency.description = data.get('description')
    agency.keywords = data.get('keywords')
    agency.common_requests = data.get('common_requests', [])
    agency.no_records_about = data.get('no_records_about', [])


def load_data(data):
    """
    Loads data from each yaml file into the database.
    """

    # Load the agency
    name = data['name']
    slug = Agency.slug_for(name)
    a, created = Agency.objects.get_or_create(slug=slug, name=name)

    # Load the agency-specific values
    load_agency_fields(a, data)

    #   If the agency only has a single department the contactable fields
    if len(data['departments']) == 1:
        dept_rec = data['departments'][0]
        contactable_fields(a, dept_rec)

    a.save()
    add_request_time_statistics(data, a)

    # Load agency offices
    if len(data['departments']) > 1:
        for dept_rec in data['departments']:

            # If top-level=True office is saved as agency
            if dept_rec.get('top_level'):
                sub_agency_name = dept_rec['name']
                sub_agency_slug = Agency.slug_for(sub_agency_name)
                sub_agency, created = Agency.objects.get_or_create(
                    slug=sub_agency_slug, name=sub_agency_name)
                sub_agency.parent = a
                load_agency_fields(sub_agency, dept_rec)
                contactable_fields(sub_agency, dept_rec)
                sub_agency.save()
                add_request_time_statistics(dept_rec, sub_agency)

            else:
                # Just an office
                office_name = dept_rec['name']
                office_slug = Office.slug_for(office_name)
                full_slug = slug + '--' + office_slug

                o, created = Office.objects.get_or_create(
                    agency=a, slug=full_slug)

                o.office_slug = office_slug
                o.name = office_name
                contactable_fields(o, dept_rec)
                o.save()
                add_request_time_statistics(dept_rec, a, o)


def process_yamls(folder):
    """
    Loops through each agency yaml file and loads it into the database
    """
    for item in iglob(folder + "/*.yaml"):
        data_file = os.path.join(folder, item)
        data = yaml.load(open(data_file))
        load_data(data)

if __name__ == "__main__":

    '''
        To run this:
        python load_agency_contacts $LOCATION_OF_DATA

        The data is currently is a folder of yaml that is in the main
        foia repo. If you were running this locally, it might look something
        like this:

        python load_agency_contacts.py ~/Projects/code/foia/foia/contacts/data

        # If you want to designate an alternate csv path, specify that as the
        # next argument following the yaml dir otherwise
        # the script will default
        # to the following:

        # ../../data/foia-contacts/full-foia-contacts/

    '''

    yaml_folder = sys.argv[1]
    process_yamls(yaml_folder)
