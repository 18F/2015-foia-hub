from docusearch.scripts.document_importer import DocImporterS3
from boto.s3.connection import S3Connection
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        aws_connection = S3Connection(
            settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = aws_connection.get_bucket(settings.DOCS_SOURCE_BUCKET)

        rs = bucket.list("", "/")
        for key in rs:
            agency = key.name.replace('/', '')
            importer = DocImporterS3(s3_bucket=bucket, agency=agency)
            importer.import_docs()
