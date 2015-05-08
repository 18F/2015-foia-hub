import os

from docusearch.scripts.document_importer import DocImporter
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import documents from your document source, into docusearch."

    def handle(self, *args, **options):
        if len(args) > 0:
            documents_directory = args[0]
            agencies = os.listdir(documents_directory)
            for agency in agencies:
                importer = DocImporter(documents_directory, agency)
                importer.import_docs()
        else:
            print('python manage.py import_documents <<document/import/path>>')
