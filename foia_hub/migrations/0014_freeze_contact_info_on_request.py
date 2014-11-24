# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import foia_hub.models
from foia_hub.models import FOIARequest


# no need to do anything on the way up
def nothing(apps, schema_editor):
    pass

# when winding down, requests made to an agency will be deleted.
def assign_offices(apps, schema_editor):
    for request in FOIARequest.objects.filter(office=None):
        request.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0013_add_request_relationship_to_agency'),
    ]

    operations = [
        # link from foia request to office is now optional.
        migrations.AlterField(
            model_name='foiarequest',
            name='office',
            field=models.ForeignKey(to='foia_hub.Office', null=True),
        ),

        # end dates was meant to be optional.
        migrations.AlterField(
            model_name='foiarequest',
            name='date_end',
            field=models.DateField(null=True)
        ),

        # Add possible emails from agency or office.
        migrations.AddField(
            model_name='foiarequest',
            name='emails',
            field=jsonfield.fields.JSONField(default=foia_hub.models.empty_list, null=True),
            preserve_default=True,
        ),

        migrations.RemoveField(
            model_name='foiarequest',
            name='custom_fields'
        ),

        # needs to be done first on the way down, before column removal above
        # invalidates the lookup call.
        migrations.RunPython(
            nothing,
            reverse_code=assign_offices
        ),

    ]
