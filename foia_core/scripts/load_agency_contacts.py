import csv
import logging
import os

import pprint

import yaml


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
    for item in os.listdir(folder):
        if count <= 2:
            data_file = os.path.join(folder, item)

            data = yaml.load(open(data_file))

            agency, created = Agency.objects.get_or_create(
                    name=data['name'],
                    abbreviation=data['abbreviation'],
                    description=data['description'],
                    )

            for dept_rec in data['departments']:
                #pprint.pprint(deptrec)

                #dict_keys(['fax', 'public_liaison', 'address', 'phone', 'service_center', 'name', 'website'])
                #'fax', 'public_liaison',



                dept, created = Department.objects.get_or_create(
                   name=dept_rec['Agency'],
                   agency=agency,
                   request_form=dept_rec.get(['request_form'], None),
                   service_center=dept_rec.get(['service_center'], None),
                   website=dept_rec.get(['website'], None),
                   address=dept_rec.get(['address'], None),
                   fax=dept_rec.get(['fax'], None),
                )

                # TODO: Access and parse service center field.
                # What is there? Is is duplicate information?

                #TODO parse and add address
                # address, created = Address.objects.get_or_create(
                #     street_address=row.get('Street Address', None),
                #     room_number=row.get('Room Number', None),
                #     city=row.get('City', None),
                #     state=row.get('State', None),
                #     zip_code=row.get('Zip Code', None),
                #     )

                # 'public_liaison'
                # TODO: Parse name & phone number from public liaison

                # 'emails'

                # pprint.pprint(dept_rec.keys())
                # try:
                #     pprint.pprint(dept_rec['public_liaison'])
                # except KeyError:
                #     pass


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
