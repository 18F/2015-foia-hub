from django.core.management.base import BaseCommand
from foia_hub.settings.default import BASE_DIR
from foia_hub.scripts.load_agency_contacts import process_yamls

# TODO: Figure out repo structure to make this generic.
# Things are moving around, leaving this here for now.

DEFAULT_YAML_FOLDER = 'foia/contacts/data'


def _get_yaml_folder():
    return BASE_DIR.rstrip('/foia_hub').rstrip('foia-') + DEFAULT_YAML_FOLDER


class Command(BaseCommand):

    help = """ Loads FOIA Contacts from YAML webscrape.
    To run with default data directory:
        django-admin.py load_agency_contacts
    Or to override the directory:
        django-admin.py load_agency_contacts path/to/data
    """

    def handle(self, *args, **options):
        try:
            yaml_folder = args[0]
        except IndexError:
            yaml_folder = _get_yaml_folder()

        process_yamls(yaml_folder)
