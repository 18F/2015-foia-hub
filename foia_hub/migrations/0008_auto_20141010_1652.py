# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0007_auto_20141010_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agency',
            old_name='examples',
            new_name='common_requests',
        ),
        migrations.RenameField(
            model_name='agency',
            old_name='counter_examples',
            new_name='no_records_about',
        ),
    ]
