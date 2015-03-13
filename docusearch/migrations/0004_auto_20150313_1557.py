# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('docusearch', '0003_document_original_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='date',
        ),
        migrations.AddField(
            model_name='document',
            name='date_created',
            field=models.DateField(null=True, help_text='Date the document was created by agency'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='file_type',
            field=models.CharField(max_length=4, help_text='File type stored in lower case ie pdf, xlsx', default='pdf'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='pages',
            field=models.IntegerField(blank=True, null=True, help_text='Number of pages in the document'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='date_released',
            field=models.DateField(help_text='Date the document was released on this site', default=datetime.date(2015, 3, 13)),
            preserve_default=False,
        ),
    ]
