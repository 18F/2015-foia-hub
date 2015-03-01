# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0018_delete_office_dups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agency',
            name='reading_room_urls',
        ),
        migrations.RemoveField(
            model_name='office',
            name='reading_room_urls',
        ),
    ]
