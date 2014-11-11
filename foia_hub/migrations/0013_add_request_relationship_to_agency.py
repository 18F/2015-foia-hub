# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0012_add_office_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='foiarequest',
            name='agency',
            field=models.ForeignKey(to='foia_hub.Agency', null=True),
            preserve_default=True,
        ),
    ]
