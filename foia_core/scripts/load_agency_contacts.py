import csv
import logging
import os

import pprint

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

    num_keys = 0
    most_keys = agency = None
    for item in os.listdir(folder):
        if count <= 2:
            data_file = os.path.join(folder, item)

            data = yaml.load(open(data_file))

            # Agencies
            name = data['name']
            slug = slugify(name[:50])
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

                office_name = dept_rec['name']
                slug = slugify(office_name[:50])
                o, created = Office.objects.get_or_create(
                    agency=a,
                    slug=slug,
                    )

                o.name = office_name
                o.request_form = dept_rec.get('request_form', None)
                o.website=dept_rec.get('website', None)
                o.service_center=dept_rec.get('service_center', None)
                o.fax=dept_rec.get('fax', None)
                o.emails=dept_rec.get('emails', None)
                o.notes=dept_rec.get('notes',None)

                #FOIA contact
                o.contact=dept_rec.get('address', None)

                #FOIA public liaison
                o.public_liaison=dept_rec.get('public_liaison', None)

                o.save()
                print(o)

                # if len(dept_rec.keys()) > num_keys:
                #     num_keys = len(dept_rec.keys())
                #     most_keys = dept_rec
                #     agency = (data['name'],data['abbreviation'],data['description'])

                # try:
                #     pprint.pprint(dept_rec['phone'])
                # except KeyError:
                #     pass

    # print(num_keys)
    # print(most_keys.keys())
    # pprint.pprint(most_keys)
    # pprint.pprint(agency)

# def process_agency_csv():
#     #TODO: Make generic as an arg when you convert to management command.
#     #folder='/Users/jacquelinekazil/Projects/code/foia/foia/contacts/data'

#     #TODO check the location; pass it as an arg
#     # when you convert to a management command.
#     folder = '/Users/jacquelinekazil/Projects/code/foia/foia-core/data/'
#     agency_or_dept = 'A'
#     csvfile = folder + 'full-foia-contacts/Agency FOIA Contacts-Table 1.csv'

#     csvdata = csv.DictReader(open(csvfile, 'rt'))

#     records_without_names = []

#     for row in csvdata:

#         #TODO: Look at records without names --
#         # make sure that you aren't losing anything.
#         name = row.get('Name', None)
#         if not name:
#             records_without_names.append(row)

#         else:
#             dept, created = Department.objects.get_or_create(
#                 name=row['Department'])

#             agency, created = Agency.objects.get_or_create(
#                 name=row['Agency'],
#                 department=dept,
#             )

#             #agency website
#             agency.website = check_urls(agency.website, row, 'Website')
#             #agency online request form
#             orf = agency.online_request_form
#             agency.online_request_form = check_urls(
#                 orf, row, 'Online Request Form')
#             agency.save()

#             address, created = Address.objects.get_or_create(
#                 street_address=row.get('Street Address', None),
#                 room_number=row.get('Room Number', None),
#                 city=row.get('City', None),
#                 state=row.get('State', None),
#                 zip_code=row.get('Zip Code', None),
#             )

#             foiacontact, created = FOIAContact.objects.get_or_create(
#                 name=row['Name'],
#                 title=row.get('Title', None),
#                 phone=row.get('Telephone', None),
#                 fax=row.get('Fax', None),
#                 email=row.get('Email Address', None).lstrip('mailto:'),
#                 location=address,
#                 agency=agency,
#                 agency_or_department=agency_or_dept,
#             )

#     print(len(records_without_names))
#     foia_titles = []
#     for rec in records_without_names:
#         foiacontacts = FOIAContact.objects.filter(

#             phone=rec['Telephone']
#         )
#         if not foiacontacts:
#             foia_titles.append(rec['Title'])
#         #print('#######################################')

#     pprint.pprint(list(set(foia_titles)))


if __name__ == "__main__":
    #process_agency_csv()
    process_yamls()
