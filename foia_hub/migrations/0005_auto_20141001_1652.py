# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0004_office_slug_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
