# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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
            field=models.DateField(help_text='Date the document was created by agency', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='date_released',
            field=models.DateField(help_text='Date the document was released by agency', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='file_type',
            field=models.CharField(default='pdf', help_text='File type stored in lower case ie pdf, xlsx', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='pages',
            field=models.IntegerField(help_text='Number of pages in the document', blank=True, null=True),
            preserve_default=True,
        ),
    ]
