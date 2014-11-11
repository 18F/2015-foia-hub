# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import foia_hub.models


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0013_add_request_relationship_to_agency'),
    ]

    operations = [
        # link from foia request to office is now optional.
        migrations.AlterField(
            model_name='foiarequest',
            name='office',
            field=models.ForeignKey(to='foia_hub.Office', null=True),
        ),

        # Add possible emails from agency or office.
        migrations.AddField(
            model_name='foiarequest',
            name='emails',
            field=jsonfield.fields.JSONField(default=foia_hub.models.empty_list, null=True),
            preserve_default=True,
        ),

    ]
