# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0019_auto_20150301_1941'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReadingRoomUrls',
        ),
    ]
