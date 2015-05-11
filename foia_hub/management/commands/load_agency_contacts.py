from django.core.management.base import BaseCommand
from foia_hub.settings.base import DEFAULT_DATA_REPO
from foia_hub.scripts.load_agency_contacts import process_yamls
import subprocess
import tempfile
import os


class Command(BaseCommand):

    help = """ Loads FOIA Contacts from YAML webscrape.
    To download the data automatically:
        django-admin.py load_agency_contacts
    Or to override the directory:
        django-admin.py load_agency_contacts path/to/data
    """

    def handle(self, *args, **options):
        if len(args) > 0:
            yaml_folder = args[0]
            process_yamls(yaml_folder)
        else:
            with tempfile.TemporaryDirectory() as tmpdirname:
                download_data(tmpdirname)
                yaml_folder = os.path.join(tmpdirname, 'contacts/data')
                process_yamls(yaml_folder)


def download_data(directory):
    subprocess.check_call(
        ["git", "clone", DEFAULT_DATA_REPO, directory], shell=False)
