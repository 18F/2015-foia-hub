#!/usr/bin/env python

import logging
import os
import re
import string
import sys

import yaml
from glob import iglob
import django
django.setup()

from foia_hub.models import Agency, Office, Stats

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


TTY_RE = re.compile('\(?\d{3}\)? \d{3}-\d{4} \(TTY\)')
ADDY_RE = re.compile('(?P<city>.*), (?P<state>[A-Z]{2}) (?P<zip>[0-9-]+)')


def clean_phone(number_str):
    """Cut down the phone number string as much as possible. If multiple
    numbers are present, take the first only"""
    number_str = number_str or ''
    number_str = number_str.replace('(', '').replace(')', '')
    number_str = number_str.replace('ext. ', 'x').replace('ext ', 'x')
    number_str = number_str.split(',')[0].strip()

    if number_str:
        return number_str


def contactable_fields(agency, office_dict):
    """Add the Contactable and USAddress fields to the agency based on values
    in the office dictionary. This will be called for both parent and child
    agencies/offices (as written in our current data set)"""
    agency.phone = clean_phone(office_dict.get('phone'))
    # a.toll_free_phone - not an explicit field in our data set
    agency.emails = office_dict.get('emails', [])
    agency.fax = clean_phone(office_dict.get('fax'))
    agency.office_url = office_dict.get('website')

    # a.reading_room_url - not an explicit field in our data set
    agency.request_form_url = office_dict.get('request_form')

    service_center = office_dict.get('service_center', '')
    match = TTY_RE.search(service_center)
    if match:
        agency.TTY_phone = match.group(0)
    #   Hack until we fix the underlying data
    if ', Phone:' in service_center:
        name = service_center[:service_center.index(', Phone:')]
    else:
        name = service_center
    agency.person_name = name or None

    public_liaison = office_dict.get('public_liaison', '')
    #   Hack until we fix the underlying data
    if ', Phone:' in public_liaison:
        name = public_liaison[:public_liaison.index(', Phone:')]
        phone = public_liaison[public_liaison.index('Phone:'):]
        phone = phone[len('Phone:'):].strip()
        # Remove TTY, if present
        match = TTY_RE.search(phone)
        if match:
            phone = phone[:match.start()].strip()
        agency.public_liaison_phone = clean_phone(phone)
    else:
        name = public_liaison
    agency.public_liaison_name = name or None

    address = office_dict.get('address', [])
    if address:
        match = ADDY_RE.match(address[-1])
        if match:
            agency.zip_code = match.group('zip')
            agency.state = match.group('state')
            agency.city = match.group('city')

        if len(address) > 1:
            agency.street = address[-2]
        if len(address) > 2:
            agency.address_lines = address[0:-2]


def add_stats(data, agency, office = None):
    '''Load stats data about agencies into the database.'''
    if not data.get('request_time_stats'):
        return
    if not data['request_time_stats'].get('2013'):
        return
    data = data['request_time_stats']['2013']

    iterator = [('S','Simple'),('C','Complex')]
    for arg in iterator:
        stat, created = Stats.objects.get_or_create(
            agency=agency, office=office, year=2013, stat_type=arg[0])
        stat.median = data.get("%s-Median No. of Days" % arg[1])
        stat.save()

def process_yamls(folder):

    #only load yaml files
    for item in iglob(folder + "/*.yaml"):

        data_file = os.path.join(folder, item)

        data = yaml.load(open(data_file))

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

        add_stats(data, a)

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
                    # Guessing at abbreviation
                    abbreviation = ''
                    for ch in sub_agency_name:
                        if ch in string.ascii_uppercase:
                            abbreviation += ch
                    sub_agency.abbreviation = abbreviation
                    sub_agency.description = dept_rec.get('description')
                    sub_agency.keyword = dept_rec.get('keywords')
                    sub_agency.common_requests = dept_rec.get(
                        'common_requests', [])
                    sub_agency.no_records_about = dept_rec.get(
                        'no_records_about', [])
                    contactable_fields(sub_agency, dept_rec)
                    sub_agency.save()

                    add_stats(dept_rec, sub_agency)
                else:
                    # Just an office
                    office_name = dept_rec['name']
                    office_slug = Office.slug_for(office_name)
                    full_slug = slug + '--' + office_slug

                    o, created = Office.objects.get_or_create(
                        agency=a, slug=full_slug)

                    o.office_slug=office_slug
                    o.name = office_name
                    contactable_fields(o, dept_rec)
                    o.save()
                    add_stats(dept_rec, a, o)


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
