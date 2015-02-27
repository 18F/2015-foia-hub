from django.core.management.base import BaseCommand
from foia_hub.models import Agency, Office, ReadingRoomUrls, Stats

# Fields found in both Agency and Office models with null values
FIELDS = (
    ('address_lines', []),
    ('emails', []),
    ('street', None),
    ('city', None),
    ('state', None),
    ('zip_code', None),
    ('phone', None),
    ('toll_free_phone', None),
    ('TTY_phone', None),
    ('fax', None),
    ('office_url', None),
    ('request_form_url', None),
    ('person_name', None),
    ('public_liaison_name', None),
    ('public_liaison_email', None),
    ('public_liaison_phone', None),
)

# Fields found only in Agency model with null values
AGENCY_FIELDS = (
    ('keywords', []),
    ('common_requests', []),
    ('no_records_about', []),
    ('abbreviation', None),
    ('chief_name', None),
    ('description', None),
)


def delete_attribute(component):

    for field in ['description', 'keywords']:
        attribute = component._meta.get_field(field)
        # attribute = None
        print(attribute.value)
    component.save()


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Deletes contact, median stat times, and reading room for
        Agencies and Offices.
        """

        Agency.objects.all().update(
            **{f: r for f, r in FIELDS + AGENCY_FIELDS})
        Office.objects.all().update(
            **{f: r for f, r in FIELDS})
        ReadingRoomUrls.objects.all().delete()
        Stats.objects.all().delete()
