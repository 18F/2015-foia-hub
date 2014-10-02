# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0002_office_top_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='office',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='office',
            name='contact_phone',
        ),
        migrations.RemoveField(
            model_name='office',
            name='emails',
        ),
        migrations.RemoveField(
            model_name='office',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='office',
            name='public_liaison',
        ),
        migrations.RemoveField(
            model_name='office',
            name='request_form',
        ),
        migrations.RemoveField(
            model_name='office',
            name='service_center',
        ),
        migrations.RemoveField(
            model_name='office',
            name='top_level',
        ),
        migrations.RemoveField(
            model_name='office',
            name='website',
        ),
        migrations.AddField(
            model_name='agency',
            name='TTY_phone',
            field=localflavor.us.models.PhoneNumberField(null=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='address_line_1',
            field=models.CharField(null=True, max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='chief_name',
            field=models.CharField(max_length=128, null=True, help_text='Name of the Chief FOIA Officer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='city',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agency',
            name='email',
            field=models.EmailField(null=True, max_length=75),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='fax',
            field=localflavor.us.models.PhoneNumberField(null=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='office_url',
            field=models.URLField(null=True, help_text='A FOIA specific URL for the office or the agency.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='parent',
            field=models.ForeignKey(null=True, to='foia_hub.Agency', help_text='Some agencies have a parent agency.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='person_name',
            field=models.CharField(null=True, max_length=250),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='phone',
            field=localflavor.us.models.PhoneNumberField(null=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='public_liaison_email',
            field=models.EmailField(null=True, max_length=75),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='public_liaison_name',
            field=models.CharField(null=True, max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='public_liaison_phone',
            field=localflavor.us.models.PhoneNumberField(null=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='reading_room_url',
            field=models.URLField(null=True, help_text='Link to repository of documents'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='request_form_url',
            field=models.URLField(null=True, help_text='If entity accepts FOIA requests online, link to the form.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='state',
            field=localflavor.us.models.USPostalCodeField(default='', max_length=2, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FM', 'Federated States of Micronesia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MH', 'Marshall Islands'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PW', 'Palau'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agency',
            name='street',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agency',
            name='toll_free_phone',
            field=localflavor.us.models.PhoneNumberField(null=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='zip_code',
            field=models.IntegerField(default=0, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='office',
            name='TTY_phone',
            field=localflavor.us.models.PhoneNumberField(null=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='address_line_1',
            field=models.CharField(null=True, max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='city',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='office',
            name='email',
            field=models.EmailField(null=True, max_length=75),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='office_url',
            field=models.URLField(null=True, help_text='A FOIA specific URL for the office or the agency.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='person_name',
            field=models.CharField(null=True, max_length=250),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='phone',
            field=localflavor.us.models.PhoneNumberField(null=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='public_liaison_email',
            field=models.EmailField(null=True, max_length=75),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='public_liaison_name',
            field=models.CharField(null=True, max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='public_liaison_phone',
            field=localflavor.us.models.PhoneNumberField(null=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='reading_room_url',
            field=models.URLField(null=True, help_text='Link to repository of documents'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='request_form_url',
            field=models.URLField(null=True, help_text='If entity accepts FOIA requests online, link to the form.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='state',
            field=localflavor.us.models.USPostalCodeField(default='', max_length=2, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FM', 'Federated States of Micronesia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MH', 'Marshall Islands'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PW', 'Palau'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='office',
            name='street',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='office',
            name='toll_free_phone',
            field=localflavor.us.models.PhoneNumberField(null=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='zip_code',
            field=models.IntegerField(default=0, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='office',
            name='fax',
            field=localflavor.us.models.PhoneNumberField(null=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='office',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='office',
            unique_together=None,
        ),
    ]
