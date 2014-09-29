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

class Contactable(models.Model):
    """ An abstract class that represents all the contactable pieces of an
    office or agency. Agencies will certainly have almost all of these fields.
    It's less clear if Offices will.  """

    phone = PhoneNumberField(null=True)
    toll_free_phone = PhoneNumberField(null=True)
    TTY_phone = PhoneNumberField(null=True)
    email = models.EmailField()
    fax = PhoneNumberField(null=True)

    office_url = models.URLField(null=True)
    reading_room_url = models.URLField(null=True)
    request_form_url = models.URLField(null=True)

    person_name = models.CharField()
    address_line1  = models.CharField()
    address_street = models.CharField()
    address_city = models.CharField()
    address_state = USPostalCodeField()
    address_zip = models.IntegerField(max_length=5)
    address_zip_four = models.IntegerField(max_length=4)

    public_liason_name = models.CharField(null=True)
    public_liason_email = models.EmailField(null=True)
    public_liason_phone = PhoneNumberField()

    class Meta:
        abstract = True


class Agency(Contactable):
    """ This represents a FOIA-able agency of the government. In some cases
    this will be a large institution like the Department of Commerce, in other
    cases it will be like the Census Bureau (which is actually part of the
    Department of Commerce)"""

    name = models.CharField(max_length=250, unique=True)
    abbreviation = models.CharField(max_length=30, null=True, unique=True)
    description = models.TextField(null=True)
    keywords = JSONField(null=True)
    slug = models.SlugField(unique=True)

    chief_name = models.CharField(null=True)

    def __str__(self):
        return 'Agency: %s' % (self.name,)

    def save(self, *args, **kwargs):
        super(Agency, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)[:50]
            super(Agency, self).save(*args, **kwargs)


class Office(Contactable):
    """ Agencies sometimes have offices that are contactable separately for
    FOIA purposes. """

    agency = models.ForeignKey(Agency)
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)

    @property
    def searchable_slug(self):
        return '%s--%s' % (self.agency.slug, self.slug)

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
