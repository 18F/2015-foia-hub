# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('text', models.TextField(help_text='The full text of the document')),
                ('title', models.TextField(null=True)),
                ('date', models.DateField(null=True)),
                ('release_agency_slug', models.CharField(help_text='Slug for the agency or office that released this document.', max_length=100)),
                ('path', models.FilePathField(help_text='Path to the original document file')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
