# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from foia_hub.models import Stats


def clear_stats(apps, schema_editor):
    """
    Need to delete old stats in case some of the old values are now
    nulls
    """
    Stats.objects.all().delete()


# no need to do anything when winding down
def nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0016_auto_20141119_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='stats',
            name='less_than_one',
            field=models.BooleanField(
                default=False,
                blank=True,
                help_text="flags when the value is `less than 1`"),
            preserve_default=True,
        ),
        migrations.RunPython(
            clear_stats,
            reverse_code=nothing
        )
    ]
