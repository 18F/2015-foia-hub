from django.core.management.base import BaseCommand, CommandError
from foia_core.models import Department, Agency, FOIAContact


class Command(BaseCommand):
    help = 'Loads FOIA Contacts from YAML webscrape & CSV'

    def handle(self, *args, **options):
        pass        