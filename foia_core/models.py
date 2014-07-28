from django.db import models


# TODO: Confirm statuses
STATUS_CHOICES = (
	('O', 'open'),
	('S', 'submitted'),
	('P', 'processing'),
	('C', 'closed'),
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

	name = models.CharField(max_length=250, unique=True)
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


class Address(models.Model):

	street_address = models.CharField(max_length=250, null=True)
	room_number = models.CharField(max_length=250, null=True)
	city = models.CharField(max_length=250, null=True)
	state = models.CharField(max_length=100, null=True)
	zip_code = models.CharField(max_length=10, null=True)


class FOIAContact(models.Model):
	name = models.CharField(max_length=150)
	title = models.CharField(max_length=250, null=True)

	phone = models.CharField(max_length=50, null=True)
	fax = models.CharField(max_length=50, null=True) 
	email = models.EmailField(null=True)

	location = models.ForeignKey(Address, null=True)
	agency = models.ForeignKey(Agency)

	def __str__(self):
		return 'FOIA Contact: %s' % (self.name,)



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

	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='O')	
	agency = models.ForeignKey('Requestor')

	request = models.TextField()

	# FEES
	#TODO: If news media, then validate news media email address?
	# How is a member legally defined? Are there other sources that we can 
	# validate against
	fee_newsmedia = models.BooleanField(default=False)  #Are you a member of media?
	fee_waiver = models.BooleanField(default=False) 	#Are you asking for a waiver?
	fee_limit = models.PositiveIntegerField() #What is the limit that the requestor is willing to pay?

	def __str__(self):
		return 'Request: %s' % (self.pk,)

