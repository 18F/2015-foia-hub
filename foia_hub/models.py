import logging

from django.db import models
from django.utils.text import slugify

from jsonfield import JSONField
from localflavor.us.models import PhoneNumberField, USPostalCodeField


logger = logging.getLogger(__name__)

# TODO: Confirm statuses
FOIA_STATUS = (
    ('O', 'open'),
    ('S', 'submitted'),
    ('P', 'processing'),
    ('C', 'closed'),
)

def empty_list():
    """Thunk for returning a *new* empty list. Must be named so that it can be
    serialized by django migrations."""
    return []


class USAddress(models.Model):
    """ An abstract representation of a United States Address."""

    address_lines = JSONField(default=empty_list)
    street = models.CharField(max_length=128, null=True)
    city = models.CharField(max_length=64, null=True)
    state = USPostalCodeField(null=True)
    zip_code = models.CharField(max_length=10, null=True)

    class Meta:
        abstract = True


class Contactable(USAddress):
    """ An abstract class that represents all the contactable pieces of an
    office or agency. Agencies will certainly have almost all of these fields.
    It's less clear if Offices will.  """

    phone = PhoneNumberField(null=True)
    toll_free_phone = PhoneNumberField(null=True)
    TTY_phone = PhoneNumberField(null=True)
    emails = JSONField(default=empty_list)
    fax = PhoneNumberField(null=True)

    office_url = models.URLField(
        null=True,
        help_text='A FOIA specific URL for the office or the agency.')

    reading_room_url = models.URLField(
        null=True, help_text='Link to repository of documents')

    request_form_url = models.URLField(
        null=True,
        help_text='If entity accepts FOIA requests online, link to the form.')

    person_name = models.CharField(max_length=250, null=True)

    public_liaison_name = models.CharField(null=True, max_length=128)
    public_liaison_email = models.EmailField(null=True)
    public_liaison_phone = PhoneNumberField(null=True)

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
    common_requests = JSONField(default=empty_list)
    no_records_about = JSONField(default=empty_list)

    parent = models.ForeignKey(
        'self',
        null=True,
        help_text='Some agencies have a parent agency.')

    chief_name = models.CharField(
        max_length=128,
        null=True, help_text='Name of the Chief FOIA Officer')

    def __str__(self):
        return 'Agency: %s' % (self.name,)

    def save(self, *args, **kwargs):
        super(Agency, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = Agency.slug_for(self.name)
            super(Agency, self).save(*args, **kwargs)

    def slug_for(text):
        """ Helper method for slugifying agency names."""
        return slugify(text)[:50]


class Office(Contactable):
    """ Agencies sometimes have offices that are contactable separately for
    FOIA purposes. """

    agency = models.ForeignKey(Agency)
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, unique=True)
    office_slug = models.SlugField(max_length=100)

    def __str__(self):
        return '%s, %s' % (self.agency.name, self.name)

    def save(self, *args, **kwargs):
        super(Office, self).save(*args, **kwargs)
        if not self.office_slug:
            self.office_slug = Office.slug_for(self.name)
        if not self.slug:
            self.slug = ('%s--%s' % (self.agency.slug, self.office_slug))[:100]
            super(Office, self).save(*args, **kwargs)

    def slug_for(text):
        """ Helper method for slugifying office names."""
        return slugify(text)[:50]


class Stats(models.Model):
    """The stats object to used to store stats pulled from reports."""

    STAT_TYPE = (
        ('S', 'simple'),
        ('C', 'complex'),
        ('E', 'expedited'),
    )

    agency = models.ForeignKey(Agency)
    office = models.ForeignKey(Office, null=True, blank=True)
    year = models.PositiveSmallIntegerField()
    stat_type =  models.CharField(max_length=1, choices=STAT_TYPE)

    average = models.FloatField(null=True, blank=True)
    median = models.FloatField(null=True, blank=True)
    high = models.FloatField(null=True, blank=True)
    low = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = (("agency", "office", "year", "stat_type"),)

    def __str__(self):
        if self.office:
            office_name = self.office.name
        else:
            office_name = None

        return '%s, %s, %s, %s' % (self.agency.name, office_name,
            self.year, self.stat_type)


class Requester(models.Model):

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class FOIARequest(models.Model):
    """
    The FOIARequest model captures a generic set of information that is
    required and/or helpful when filing federal Freedom of Information
    Act requests.

    There are currently no facilities for agency- or office-specific fields,
    as our current target is providing a basic webform for those offices that
    do not provide one themselves.

    A FOIARequest contains a number of informational fields about the request.
    It also contains a foreign key to the agency or office the request was to.

    However, this is for reference and not dereference -- the contact details
    for the agency or office the request was to is copied onto the FOIARequest
    at creation time, so that even if an Agency or Office's contact data
    changes later, we maintain an accurate record of where and how the
    request was sent.
    """
    status = models.CharField(max_length=1, choices=FOIA_STATUS, default='O')

    requester = models.ForeignKey(Requester)

    # which office or agency this went to
    office = models.ForeignKey(Office, null=True)
    agency = models.ForeignKey(Agency, null=True)
    # the relevant email addresses this went to.
    # TODO: for now, it can be null, but we need firmer policy on what to do.
    emails = JSONField(null=True)

    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)

    # Fee limit requester is willing to pay without consultation.
    fee_limit = models.PositiveIntegerField(default=0)

    request_body = models.TextField()

    def __str__(self):
        return '%s' % (self.pk,)
