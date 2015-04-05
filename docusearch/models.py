import os

from django.db import models
from django.utils.timezone import now
from storages.backends.s3boto import S3BotoStorage

AWS_STORAGE_DOC_BUCKET = os.getenv('FOIA_S3_DOCS_BUCKET_NAME')


def upload_original_to(instance, filename):
    """ Return the path this file should be stored at. """

    filename_base, filename_ext = os.path.splitext(filename)
    filename_ext = filename_ext.lower()

    origin_path = instance.release_agency_slug
    if '--' in instance.release_agency_slug:
        agency_slug, office_slug = instance.release_agency_slug.split('--')
        origin_path = '%s/%s' % (agency_slug, office_slug)

    right_now = now().strftime("%Y%m%d%H%M")

    upload_path = '%s/%s/%s%s' % (
        origin_path, right_now, filename_base, filename_ext)
    return upload_path


class Document(models.Model):
    """
    A model representing a document from an agency. It also uploads documents
    to a different bucket than the static files by setting a specific bucket
    `storage=S3BotoStorage(bucket=AWS_STORAGE_DOC_BUCKET)`
    """

    text = models.TextField(
        null=False, help_text='The full text of the document')
    title = models.TextField(null=True)
    date_created = models.DateField(
        blank=True, null=True,
        help_text='Date the document was created by agency')
    date_released = models.DateField(
        blank=True, null=True,
        help_text='Date the document was released by agency')
    pages = models.IntegerField(
        blank=True, null=True, help_text='Number of pages in the document')
    file_type = models.CharField(
        max_length=4, help_text='File type stored in lower case ie pdf, xlsx')
    release_agency_slug = models.CharField(
        max_length=100,
        help_text="Slug for the agency or office that released this document.")

    if AWS_STORAGE_DOC_BUCKET:
        original_file = models.FileField(
            upload_to=upload_original_to, blank=True, null=True,
            storage=S3BotoStorage(bucket=AWS_STORAGE_DOC_BUCKET))
    else:
        original_file = models.FileField(
            upload_to=upload_original_to, blank=True, null=True)

    def get_absolute_url(self):
        """ Return the canonical URL for a Document object. """
        return '/documents/document/%i' % self.id


class ImportLog(models.Model):
    """ A model that helps keep track of what directories have been processed
    by the importer (so we don't process them again). """

    agency_slug = models.CharField(max_length=100)
    office_slug = models.CharField(max_length=100, null=True)

    # This is typically a date, but if we have multiple directories on a day it
    # might have a suffix. E.g. 20150102-2
    directory = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('agency_slug', 'office_slug', 'directory')
        index_together = ('agency_slug', 'office_slug', 'directory')
