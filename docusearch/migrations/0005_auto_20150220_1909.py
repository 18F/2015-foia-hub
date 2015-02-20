# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docusearch', '0004_remove_document_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='create_date',
            field=models.DateField(help_text='The date this document was created', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='release_date',
            field=models.DateField(help_text='The date this document was released to the public', null=True),
            preserve_default=True,
        ),
    ]
