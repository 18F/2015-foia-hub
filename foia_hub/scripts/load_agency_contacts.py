import csv
import logging
import os
import sys

import yaml

from django.utils.text import slugify

from foia_hub.models import *

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


def process_yamls(folder):

    for item in os.listdir(folder):
        data_file = os.path.join(folder, item)

        data = yaml.load(open(data_file))

        # Agencies
        name = data['name']
        slug = slugify(name)[:50]

        a, created = Agency.objects.get_or_create(slug=slug, name=name)

        a.abbreviation = data['abbreviation']
        a.description = data.get('description', None)
        a.save()

        # Offices
        for dept_rec in data['departments']:
            """
            Data mapping
            name = name
            request_form = request_form
            website = website
            service_center = service_center
            fax = fax
            emails = emails
            notes = notes
            contact = address (name, title, address, etc.)
            contact_phone = parsed from address

            public_liaison = public_liaison
            """

            office_name = dept_rec['name']
            slug = slugify(office_name)[:50]
            o, created = Office.objects.get_or_create(
                agency=a,
                slug=slug,
            )

            o.name = office_name
            o.request_form = dept_rec.get('request_form', None)
            o.website = dept_rec.get('website', None)
            o.service_center = dept_rec.get('service_center', None)
            o.phone = dept_rec.get('phone', None)
            o.fax = dept_rec.get('fax', None)
            o.emails = dept_rec.get('emails', None)
            o.notes = dept_rec.get('notes', None)

            #FOIA contact
            o.contact = dept_rec.get('address', None)

            #FOIA public liaison
            o.public_liaison = dept_rec.get('public_liaison', None)

            o.save()


def process_agency_csv(data_path):

    csvdata = csv.DictReader(open(csvfile, 'rt'))

    """
    {'Agency': 'Administrative Conference of the United States',
     'City': 'Washington',
     'Department': 'Administrative Conference of the United States',
     'Email Address': '',
     'Fax': '(202) 386-7190',
     'Name': 'Shawne McGibbon',
     'Notes': '',
     'Online Request Form': '',
     'Room Number': 'Suite 706 South',
     'State': 'DC',
     'Street Address': '1120 20th Street, NW',
     'Telephone': '(202) 480-2088',
     'Title': 'FOIA Officer',
     'Website': 'http://www.acus.gov/foia/',
     'Zip Code': '20036'}
     """

    for row in csvdata:

        # Agencies
        name = row['Department']
        slug = slugify(name)[:50]
        a, created = Agency.objects.get_or_create(
            slug=slug, name=name
        )
        a.save()

        # Offices
        office_name = row['Agency']
        slug = slugify(office_name)[:50]
        o, created = Office.objects.get_or_create(
            agency=a, slug=slug, name=office_name
        )

        o.website = row.get('website', None)
        o.request_form = row.get('Online Request Form', None)
        o.fax = row.get('fax', None)
        o.notes = row.get('notes', None)
        o.save()

        # Person
        zip_code = row.get('Zip Code', None)
        phone = row.get('Telephone', None)
        email = row.get('Email Address', None)
        state = row.get('State', None)

        # Only create a person record if these exist
        if name or title:
            if zip_code or phone or email or state:

                # To fix the following record and any like it.
                # "20857(if sending by courier use zc 20814)"
                if len(zip_code) > 10:
                    zip_code = zip_code[:5]

                # To fix the following record and any like it.
                # '(800) 375-5283 (USCIS National Customer Service Unit)'
                if len(phone) > 50:
                    phone = phone[:14]

                # Note: Some phone fields have 2 phone numbers.
                # Not sure if one is more important the other.
                # TODO: Compare if one these numbers is stored with other
                # person, so it doesn't need to be stored with this on.
                # example: (202) 343-1743, (866) 431-0486

                person = Person(
                    email=email, phone=phone,

                    name=row.get('Name', None),
                    title=row.get('Title', None),

                    street_address=row.get('Street Address', None),
                    room_number=row.get('Room Number', None),
                    city=row.get('City', None),

                    state=state, zip_code=zip_code,

                    office=o,
                )
                person.save()

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

    # # Overlay csv file information on the yaml info
    # try:
    #     csv_folder = sys.argv[2]
    # except IndexError:
    #     csv_folder = "../../data/foia-contacts/full-foia-contacts/"
    #     print('No csv folder passed as arg.')
    #     print('Setting to default %s.' % csv_folder)

    for item in os.listdir(folder):
        data_file = os.path.join(folder, item)
        process_agency_csv(data_file)
