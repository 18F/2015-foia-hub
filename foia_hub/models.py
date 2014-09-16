import logging
from django.db import models

from django.utils.text import slugify
from jsonfield import JSONField


logger = logging.getLogger(__name__)

# TODO: Confirm statuses
FOIA_STATUS = (
    ('O', 'open'),
    ('S', 'submitted'),
    ('P', 'processing'),
    ('C', 'closed'),
)

# PERSON_TYPE = (
#     ('S', 'contact'),
#     ('L', 'liaison'),
#     ('C', 'chief'),
#     ('B', 'Both'),
# )


class Agency(models.Model):

    name = models.CharField(max_length=250, unique=True)
    abbreviation = models.CharField(max_length=30, null=True, unique=True)
    description = models.TextField(null=True)
    keywords = JSONField(null=True)
    slug = models.SlugField(unique=True)
    # dept = models.BooleanField()  # This is from csv - possibly removable
    # chief_foia_officer

    def __str__(self):
        return 'Agency: %s' % (self.name,)

    def save(self, *args, **kwargs):
        super(Agency, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)[:50]
            super(Agency, self).save(*args, **kwargs)


class Office(models.Model):

    agency = models.ForeignKey(Agency)
    name = models.CharField(max_length=250)
    slug = models.SlugField()

    # phone numbers
    service_center = models.CharField(max_length=250, null=True)
    fax = models.CharField(max_length=50, null=True)

    # electronic comms
    request_form = models.URLField(null=True)
    website = models.URLField(null=True)
    emails = models.CharField(max_length=250, null=True)

    # public contact
    contact = models.TextField(null=True)  # address
    contact_phone = models.CharField(max_length=50, null=True)  # phone

    # Public liaison
    public_liaison = models.TextField(null=True)

    notes = models.TextField(null=True)

    def __str__(self):
        return '%s, %s' % (self.agency.name, self.name)

    class Meta:
        unique_together = (("slug", "agency"),)

    def save(self, *args, **kwargs):
        super(Office, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)[:50]
            super(Office, self).save(*args, **kwargs)



class Requester(models.Model):

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class FOIARequest(models.Model):

    status = models.CharField(max_length=1, choices=FOIA_STATUS, default='O')

    requester = models.ForeignKey(Requester)
    office = models.ForeignKey(Office)

    date_start = models.DateField(null=True)
    date_end = models.DateField(null=False)

    # Fee limit requester is willing to pay without consultation.
    fee_limit = models.PositiveIntegerField(default=0)

    request_body = models.TextField()
    custom_fields = JSONField(null=True)

    def __str__(self):
        return '%s' % (self.pk,)
