from django.core.management.base import BaseCommand
from foia_hub.settings.base import BASE_DIR, DEFAULT_DATA_REPO
from foia_hub.scripts.load_agency_contacts import process_yamls
import os
import shutil
import subprocess

class Command(BaseCommand):

    help = """ Loads FOIA Contacts from YAML webscrape.
    To run with default data directory:
        django-admin.py load_agency_contacts
    Or to override the directory:
        django-admin.py load_agency_contacts path/to/data
    """

    def handle(self, *args, **options):
        if len(args) > 0:
            yaml_folder = args[0]
        else:
            yaml_folder = download_data()

        print("Data directory: %s" % yaml_folder)
        print("Loading data...")
        process_yamls(yaml_folder)

# Clone a new copy of the git repo, removing the dir if it exists.
def download_data():
    print("No directory given, checking out copy of data from version control.")
    print("Note: this requires git to be installed.")

    path = temp_home()
    if os.path.exists(path):
        print("Deleting old data checkout.")
        shutil.rmtree(path)

    print("Cloning repository at %s" % DEFAULT_DATA_REPO)
    clone_repo(DEFAULT_DATA_REPO, path)

    return os.path.join(path, "contacts", "data")

def temp_home():
    return os.path.join(BASE_DIR, "..", "temp-data")

# test if a command exists, don't print output
def clone_repo(repo, directory):
    subprocess.check_call(["git", "clone", repo, directory], shell=False)
