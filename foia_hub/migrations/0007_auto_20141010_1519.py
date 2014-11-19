# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields
import foia_hub.models


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0006_auto_20141002_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='counter_examples',
            field=jsonfield.fields.JSONField(default=foia_hub.models.empty_list),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='examples',
            field=jsonfield.fields.JSONField(default=foia_hub.models.empty_list),
            preserve_default=True,
        ),
    ]
