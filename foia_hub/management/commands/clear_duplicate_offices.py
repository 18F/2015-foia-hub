from django.core.management.base import BaseCommand
from foia_hub.models import Agency, Office


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Deletes offices that have a sub-agency equivalent.
        """

        agencies = Agency.objects.exclude(
            parent__isnull=True).values_list("name")
        offices = Office.objects.values_list("name").all()
        duplicate_offices = list(set(agencies) & set(offices))
        for office_name in duplicate_offices:
            office = Office.objects.get(name=office_name[0])
            office.delete()
