# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import docusearch.models


class Migration(migrations.Migration):

    dependencies = [
        ('docusearch', '0002_remove_document_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='original_file',
            field=models.FileField(upload_to=docusearch.models.upload_original_to, blank=True, null=True),
            preserve_default=True,
        ),
    ]
