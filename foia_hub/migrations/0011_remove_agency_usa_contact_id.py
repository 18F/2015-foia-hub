# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0010_addresses_and_emails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agency',
            name='usa_contact_id',
        ),
    ]
