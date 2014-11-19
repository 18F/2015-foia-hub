# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields
import foia_hub.models


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0009_agency_usa_contact_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='emails',
            field=jsonfield.fields.JSONField(default=foia_hub.models.empty_list),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='address_lines',
            field=jsonfield.fields.JSONField(default=foia_hub.models.empty_list),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='emails',
            field=jsonfield.fields.JSONField(default=foia_hub.models.empty_list),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='address_lines',
            field=jsonfield.fields.JSONField(default=foia_hub.models.empty_list),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='agency',
            name='email'
        ),
        migrations.RemoveField(
            model_name='agency',
            name='address_line_1'
        ),
        migrations.RemoveField(
            model_name='office',
            name='email'
        ),
        migrations.RemoveField(
            model_name='office',
            name='address_line_1'
        )
    ]
