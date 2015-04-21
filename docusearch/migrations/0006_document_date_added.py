# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('docusearch', '0005_auto_20150331_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='date_added',
            field=models.DateField(default=datetime.date(2015, 4, 21), help_text='Date the document was added to database'),
            preserve_default=False,
        ),
    ]
