# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from foia_hub.models import Agency, Office


def clear_duplicated_offices(apps, schema_editor):
    """
    Deletes offices that have a sub-agency equivalent.
    """
    agencies = Agency.objects.exclude(parent__isnull=True).values_list("name")
    offices = Office.objects.values_list("name").all()
    duplicate_offices = list(set(agencies) & set(offices))
    for office_name in duplicate_offices:
        office = Office.objects.get(name=office_name[0])
        office.delete()


# no need to do anything when winding down
def nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0017_stats_less_than_one'),
    ]

    operations = [
        migrations.RunPython(
            clear_duplicated_offices,
            reverse_code=nothing
        )
    ]
