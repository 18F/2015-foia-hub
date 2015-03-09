from django.core.management.base import BaseCommand
from foia_hub.settings.base import BASE_DIR, DEFAULT_DATA_REPO
from foia_hub.scripts.load_agency_contacts import process_yamls
import os
import shutil
import subprocess

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
        else:
            yaml_folder = download_data(self)

        self.stdout.write("Data directory: %s" % yaml_folder)
        self.stdout.write("Loading data...")
        process_yamls(yaml_folder)

# Clone a new copy of the git repo, removing the dir if it exists.
def download_data(command):
    command.stdout.write("No directory given, checking out copy of data from version control.")
    command.stdout.write("Note: this requires git to be installed.")

    path = temp_home()
    if os.path.exists(path):
        command.stdout.write("Deleting old data checkout.")
        shutil.rmtree(path)

    command.stdout.write("Cloning repository at %s" % DEFAULT_DATA_REPO)
    clone_repo(DEFAULT_DATA_REPO, path)

    return os.path.join(path, "contacts", "data")

def temp_home():
    return os.path.join(BASE_DIR, "..", "temp-data")

def clone_repo(repo, directory):
    subprocess.check_call(["git", "clone", repo, directory], shell=False)
