# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify

# This migration uses `slugify(office.name)[:50]` instead of
# calling `Office.slug_for(office.name)` so that its operation
# is frozen at how slugifying worked at the time of this migration,
# not at whatever Office.slug_for currently does.

def initialize_office_slugs(apps, schema_editor):
    """ Make the Office slugs unique. """
    Office = apps.get_model("foia_hub", "Office")
    db_alias = schema_editor.connection.alias

    for office in Office.objects.using(db_alias).all():
        office.office_slug = slugify(office.name)[:50]
        office.save()

# they'll get removed when the field gets removed
def remove_office_slugs(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0011_remove_agency_usa_contact_id'),
    ]

    operations = [
        # first, add the new office_slug field, temporarily allow NULL
        migrations.AddField(
            model_name='office',
            name='office_slug',
            field=models.SlugField(max_length=100, null=True),
        ),

        # then, give them an initial value
        migrations.RunPython(
            initialize_office_slugs,
            reverse_code=remove_office_slugs
        ),

        # finally, remove the NULL constraint
        migrations.AlterField(
            model_name='office',
            name='office_slug',
            field=models.SlugField(max_length=100, null=False),
        ),
    ]
