import csv
import logging
import os

import yaml

from django.utils.text import slugify


from foia_core.models import *

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


def process_yamls():

    folder = '/Users/jacquelinekazil/Projects/code/foia/foia/contacts/data'

    count = 0

    # num_keys = 0
    # most_keys = agency = None
    for item in os.listdir(folder):
        if count <= 2:
            data_file = os.path.join(folder, item)

            data = yaml.load(open(data_file))

            # Agencies
            name = data['name']
            slug = slugify(name)[:50]
            a, created = Agency.objects.get_or_create(slug=slug, name=name)

            a.abbreviation = data['abbreviation'],
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

                name = dept_rec['name']
                slug = slugify(name)[:50]
                o, created = Office.objects.get_or_create(
                    agency=a,
                    slug=slug,
                )

                o.name = office_name
                o.request_form = dept_rec.get('request_form', None)
                o.website = dept_rec.get('website', None)
                o.service_center = dept_rec.get('service_center', None)
                o.fax = dept_rec.get('fax', None)
                o.emails = dept_rec.get('emails', None)
                o.notes = dept_rec.get('notes', None)

                #FOIA contact
                o.contact = dept_rec.get('address', None)

                #FOIA public liaison
                o.public_liaison = dept_rec.get('public_liaison', None)

                o.save()

                # if len(dept_rec.keys()) > num_keys:
                #     num_keys = len(dept_rec.keys())
                #     most_keys = dept_rec
                #     agency = (data['name'],
                #        data['abbreviation'],data['description'])

                # try:
                #     pprint.pprint(dept_rec['phone'])
                # except KeyError:
                #     pass


def process_agency_csv(folder, filepath, dept):

    csvfile = folder + filepath

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
            slug=slug, name=name,  dept = dept
        )
        a.dept = dept
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
        if zip_code or phone or email or state:
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


    #TODO: Make generic as an arg when you convert to management command.
    #folder='/Users/jacquelinekazil/Projects/code/foia/foia/contacts/data'

    #TODO check the location; pass it as an arg
    # when you convert to a management command.
    folder = '/Users/jacquelinekazil/Projects/code/foia/foia-core/data/'
    filepath = 'full-foia-contacts/Agency FOIA Contacts-Table 1.csv'
    dept = False

    process_agency_csv(folder, filepath, dept)

    filepath = 'full-foia-contacts/Dept. FOIA Contacts-Table 1.csv'
    dept = True

    process_agency_csv(folder, filepath, dept)




    #process_yamls()
