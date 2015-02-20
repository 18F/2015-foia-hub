import os

from django.db import models
from django.utils.timezone import now


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
    """ A model representing a document from an agency. """

    text = models.TextField(
        null=False, help_text='The full text of the document')
    title = models.TextField(null=True)
    date = models.DateField(null=True)
    release_agency_slug = models.CharField(
        max_length=100,
        help_text="Slug for the agency or office that released this document.")
    original_file = models.FileField(
        upload_to=upload_original_to, blank=True, null=True)

    def get_absolute_url(self):
        """ Return the canonical URL for a Document object. """

        return '/documents/document/%i' % self.id
