# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.utils.text import slugify

# These migrations uses `slugify(office.name)[:50]` instead of
# calling `Office.slug_for(office.name)` so that their operation
# is frozen at how slugifying worked at the time of this migration,
# not at whatever Office.slug_for currently does.

def change_office_slugs(apps, schema_editor):
    """ Make the Office slugs unique. """
    Office = apps.get_model("foia_hub", "Office")
    db_alias = schema_editor.connection.alias

    for office in Office.objects.using(db_alias).all():
        office_slug = slugify(office.name)[:50]
        office.slug = ('%s--%s' % (office.agency.slug, office_slug))[:100]
        office.save()

def reverse_office_slugs(apps, schema_editor):
    Office = apps.get_model("foia_hub", "Office")
    db_alias = schema_editor.connection.alias

    for office in Office.objects.using(db_alias).all():
        office_slug = slugify(office.name)[:50]
        office.slug = office_slug
        office.save()

class Migration(migrations.Migration):
    dependencies = [
        ('foia_hub', '0003_auto_20141001_1633')
    ]

    operations = [
        migrations.RunPython(
            change_office_slugs,
            reverse_code=reverse_office_slugs
        )
    ]
