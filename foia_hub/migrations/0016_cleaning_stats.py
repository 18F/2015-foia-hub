# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from foia_hub.models import Stats
import jsonfield.fields

# one-way street
def clear_empty_stats(apps, schema_editor):
    for stat in Stats.objects.filter(median=None):
        stat.delete()

# no need to do anything on the way up
def nothing(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0015_adding_stats_obj'),
    ]

    operations = [
        migrations.RunPython(
            clear_empty_stats,
            reverse_code=nothing
        ),
    ]
