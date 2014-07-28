import csv
import logging
import os

import pprint
import yaml

from foia_core.models import Department, Agency, Address, FOIAContact

logger = logging.getLogger("load_agency_contacts")


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
        return  row_url

def process_agency_csv():
    #TODO: Make generic as an arg when you convert to management command.
    #folder='/Users/jacquelinekazil/Projects/code/foia/foia/contacts/data'

    #TODO check the location; pass it as an arg when you convert to a management command. 
    folder = '/Users/jacquelinekazil/Projects/code/foia/foia-core/data/'
    csvfile = folder + 'full-foia-contacts/Agency FOIA Contacts-Table 1.csv'

    csvdata = csv.DictReader(open(csvfile,'rt'))

    records_to_hold = []

    for row in csvdata:

        #TODO: Look at records without names -- make sure that you aren't losing
        # anything.
        name = row.get('Name', None)
        if not name:
            records_to_hold.append(row)

        else:
            dept, created = Department.objects.get_or_create(name=row['Department'])

            agency, created = Agency.objects.get_or_create(
                name = row['Agency'],
                department = dept,
            )

            #agency website
            agency.website = check_urls(agency.website, row, 'Website')
            #agency online request form
            orf = agency.online_request_form
            agency.online_request_form = check_urls(orf, row, 'Online Request Form')
            agency.save()

            address, created = Address.objects.get_or_create(
                street_address = row.get('Street Address', None),
                room_number = row.get('Room Number', None),
                city = row.get('City', None),
                state = row.get('State', None),
                zip_code = row.get('Zip Code', None),
                )

            foiacontact, created = FOIAContact.objects.get_or_create(
                name = row['Name'],
                title = row.get('Title', None),
                phone = row.get('Telephone', None),
                fax = row.get('Fax', None),
                email = row.get('Email Address', None).lstrip('mailto:'),
                location = address, 
                agency = agency,
                )

    pprint.pprint(records_to_hold)
    print(len(records_to_hold))


if __name__ == "__main__":
    process_agency_csv()