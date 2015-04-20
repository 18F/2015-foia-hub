from boto.s3.connection import S3Connection
from django.core.management.base import BaseCommand
from django.conf import settings

import yaml

from .document_importer import is_date


def last_name_in_path(path):
    """
    Returns the last name in a path. 

    'doc/20150301/' returns 20150301
    'doc/20150301/abc.pdf' returns abc.pdf
    """
    path_split = path.rsplit('/')

    if path_split[-1] == '':
        return path_split[-2]
    else:
        return path_split[-1]


class Command(BaseCommand):

    help = """Import documents from your document source S3 bucket, into
    docusearch. """

    def read_manifest(self, directory_prefix):
        """ Given the path to an agency's date directory, return a parsed
        manifest file if it exists. """

        manifest_name = directory_prefix.name + 'manifest.yaml'
        manifest_key = directory_prefix.bucket.get_key(manifest_name)

        if manifest_key:
            manifest = yaml.load(manifest_key.get_contents_as_string())
            return manifest

    #we might want to rename this to: "read_manifest"
    def process_date_documents(self, agency, date_directory, directory_prefix):
        """ 
        agency example: 'department-of-commerce/'

        date_directory: '20150331'

        directory_prefix: boto.s3.prefix.Prefix object. directory_prefix.name 
        returns '/department-of-commerce/20150331/'
        """

        manifest = self.read_manifest(directory_prefix)
        print(manifest)


    def handle(self, *args, **options):

        aws_connection = S3Connection(
            settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        self.bucket = aws_connection.get_bucket(settings.DOCS_SOURCE_BUCKET)

        rs = self.bucket.list("", "/")

        for key in rs:
            agency = key.name

            ts = self.bucket.list(agency, "/")
            for asd in ts:
                agency_sub_directory = last_name_in_path(asd.name)
                if is_date(agency_sub_directory):
                    self.process_date_documents(agency, agency_sub_directory, asd)
