# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docusearch', '0004_auto_20150318_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('agency_slug', models.CharField(max_length=100)),
                ('office_slug', models.CharField(null=True, max_length=100)),
                ('directory', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='importlog',
            unique_together=set([('agency_slug', 'office_slug', 'directory')]),
        ),
        migrations.AlterIndexTogether(
            name='importlog',
            index_together=set([('agency_slug', 'office_slug', 'directory')]),
        ),
    ]
