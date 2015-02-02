#!/usr/bin/env python

import logging
import os
import string
import sys

import yaml
from glob import iglob
import django
django.setup()

from foia_hub.models import Agency, Office, Stats, ReadingRoomUrls

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
    if 'name' in service_center:
        agency.person_name = service_center['name']

    public_liaison = office_dict.get(
        'public_liaison', {'name': None, 'phone': []})
    agency.public_liaison_phone = extract_non_tty_phone(public_liaison)
    if 'name' in public_liaison:
        agency.public_liaison_name = public_liaison['name']

    address = office_dict.get('address', {})
    if address:
        agency.zip_code = address['zip']
        agency.state = address['state']
        agency.city = address['city']
        agency.street = address['street']
        if 'address_lines' in address:
            agency.address_lines = address['address_lines']

    reading_rooms = office_dict.get('reading_rooms', [])
    if reading_rooms:
        add_reading_rooms(agency, reading_rooms)


def add_request_time_statistics(data, agency, office=None):
    '''Load stats data about agencies into the database.'''
    if not data.get('request_time_stats'):
        return
    latest_year = sorted(
        data.get('request_time_stats').keys(), reverse=True)[0]
    data = data['request_time_stats'].get(latest_year)
    if not data:
        return
    iterator = [('S', 'simple'), ('C', 'complex')]
    for arg in iterator:
        median = data.get("%s_median_days" % arg[1])
        if median:
            stat, created = Stats.objects.get_or_create(
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


def add_reading_rooms(contactable, reading_rooms):
    for link_text, url in reading_rooms:
        existing_room = ReadingRoomUrls.objects.filter(
            link_text=link_text, url=url)
        existing_room = list(existing_room)
        if len(existing_room) > 0:
            contactable.reading_room_urls.add(*existing_room)
        else:
            r = ReadingRoomUrls(link_text=link_text, url=url)
            r.save()
            contactable.reading_room_urls.add(r)
    return contactable


def build_abbreviation(agency_name):
    """ Given an agency name, guess at an abbrevation. """
    abbreviation = ''
    for ch in agency_name:
        if ch in string.ascii_uppercase:
            abbreviation += ch
    return abbreviation


def load_data(data):
    """
    Loads data from each yaml file into the database.
    """

    # Agencies
    name = data['name']
    slug = Agency.slug_for(name)

    a, created = Agency.objects.get_or_create(slug=slug, name=name)

    a.abbreviation = data['abbreviation']
    a.description = data.get('description')
    a.keywords = data.get('keywords')
    a.common_requests = data.get('common_requests', [])
    a.no_records_about = data.get('no_records_about', [])

    #   Only has a single, main branch/office
    if len(data['departments']) == 1:
        dept_rec = data['departments'][0]
        contactable_fields(a, dept_rec)

    a.save()
    add_request_time_statistics(data, a)

    # Offices
    if len(data['departments']) > 1:
        for dept_rec in data['departments']:
            if dept_rec.get('top_level'):
                # This is actually an agency
                sub_agency_name = dept_rec['name']
                sub_agency_slug = Agency.slug_for(sub_agency_name)

                sub_agency, created = Agency.objects.get_or_create(
                    slug=sub_agency_slug, name=sub_agency_name)
                sub_agency.parent = a

                abbreviation = dept_rec.get('abbreviation')
                if not abbreviation:
                    abbreviation = build_abbreviation(sub_agency_name)
                sub_agency.abbreviation = abbreviation

                sub_agency.description = dept_rec.get('description')
                sub_agency.keywords = dept_rec.get('keywords')
                sub_agency.common_requests = dept_rec.get(
                    'common_requests', [])
                sub_agency.no_records_about = dept_rec.get(
                    'no_records_about', [])
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
