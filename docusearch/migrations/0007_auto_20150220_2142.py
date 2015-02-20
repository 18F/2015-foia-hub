# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docusearch', '0006_importlog'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='importlog',
            unique_together=set([('agency_slug', 'office_slug', 'directory')]),
        ),
        migrations.AlterIndexTogether(
            name='importlog',
            index_together=set([('agency_slug', 'office_slug', 'directory')]),
        ),
    ]
