# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0014_freeze_contact_info_on_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foiarequest',
            name='emails',
            field=jsonfield.fields.JSONField(null=True),
        ),
    ]
