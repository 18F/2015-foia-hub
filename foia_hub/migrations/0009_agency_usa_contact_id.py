# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0008_auto_20141010_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='usa_contact_id',
            field=models.IntegerField(null=True, help_text='usa.gov contacts api id.'),
            preserve_default=True,
        ),
    ]
