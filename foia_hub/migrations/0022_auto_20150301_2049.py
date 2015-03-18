# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('foia_hub', '0021_readingroomurls'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readingroomurls',
            name='agency',
        ),
        migrations.RemoveField(
            model_name='readingroomurls',
            name='office',
        ),
        migrations.AddField(
            model_name='readingroomurls',
            name='content_type',
            field=models.ForeignKey(default=0, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='readingroomurls',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
