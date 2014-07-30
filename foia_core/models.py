import logging
from django.db import models


logger = logging.getLogger(__name__)

# TODO: Confirm statuses
FOIA_STATUS = (
    ('O', 'open'),
    ('S', 'submitted'),
    ('P', 'processing'),
    ('C', 'closed'),
)

CONTACT_STATUS = (
    ('A', 'Agency'),
    ('D', 'Department')
)

#TODO: Add slug to almost everything that could be a page, the
# population that slug


class Department(models.Model):

    name = models.CharField(max_length=250, unique=True)
    abbreviation = models.CharField(max_length=10, null=True, unique=True)
    description = models.TextField(null=True)

    def __str__(self):
        return 'Dept: %s' % (self.name,)


class Agency(models.Model):

    name = models.CharField(max_length=250)
    #phone = models.CharField(max_length=12)
    #service_center = models.CharField(max_length=12, null=True)

    online_request_form = models.URLField(null=True)
    website = models.URLField(null=True)

    department = models.ForeignKey(Department)

    # TODO: Many of the notes may just be the following:
    # 'This agency has additional FOIA contact information
    # that can be found by visiting its website.'
    # Check the notes field and turn into Boolean if this is consistant.
    notes = models.TextField(null=True)

    def __str__(self):
        return 'Agency: %s' % (self.name,)

    class Meta:
        unique_together = (("name", "department"),)


class Address(models.Model):

    street_address = models.CharField(max_length=250, null=True)
    room_number = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=250, null=True)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True)


class FOIAContact(models.Model):

    name = models.CharField(max_length=150, null=True)
    title = models.CharField(max_length=250, null=True)

    phone = models.CharField(max_length=50, null=True)
    fax = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)

    location = models.ForeignKey(Address, null=True)
    agency = models.ForeignKey(Agency)

    # The original spreadsheet of contacts had two tabs.
    # One tab was 'Agency', the other was 'Department'
    # The difference was not clear between the contacts, but
    # the tabs contained unique information, so that was stored.
    # This field means nothing more than that.
    agency_or_department = models.CharField(max_length=1,
                                            choices=CONTACT_STATUS,
                                            null=True)

    def __str__(self):
        return 'FOIA Contact: %s' % (self.name,)

    def save(self, *args, **kwargs):
        """
        This is to make sure that there is either a name or title.
        Some titles don't have names and some names don't have titles.
        """

        if self.name or self.title:
            super(FOIAContact, self).save(*args, **kwargs)
        else:
            logger.warning('%s not saved, because no title or name' % self)


class Requestor(models.Model):

    # TODO: name clarification -- first & last or one field?
    #first_name = Charfield.models(max_length=100)
    #last_name = models.Charfield(max_length=100)
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=10)
    email = models.EmailField()

    #TODO: Add address fields or can we do this without?

    def __str__(self):
        return 'Requestor: %s' % (self.name,)


class FOIARequest(models.Model):

    status = models.CharField(max_length=1, choices=FOIA_STATUS, default='O')
    agency = models.ForeignKey('Requestor')

    request = models.TextField()

    # FEES
    #TODO: If news media, then validate news media email address?
    # How is a member legally defined? Are there other sources that we can
    # validate against
    fee_newsmedia = models.BooleanField(default=False)  # member of media?
    fee_waiver = models.BooleanField(default=False) 	# asking for a waiver?
    fee_limit = models.PositiveIntegerField()  # limit requestor willing to pay

    def __str__(self):
        return 'Request: %s' % (self.pk,)
