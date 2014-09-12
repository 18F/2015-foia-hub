# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('abbreviation', models.CharField(max_length=30, unique=True, null=True)),
                ('description', models.TextField(null=True)),
                ('keywords', jsonfield.fields.JSONField(null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FOIARequest',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.CharField(choices=[('O', 'open'), ('S', 'submitted'), ('P', 'processing'), ('C', 'closed')], default='O', max_length=1)),
                ('date_start', models.DateField(null=True)),
                ('date_end', models.DateField()),
                ('fee_limit', models.PositiveIntegerField(default=0)),
                ('request_body', models.TextField()),
                ('custom_fields', jsonfield.fields.JSONField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField()),
                ('service_center', models.CharField(max_length=250, null=True)),
                ('fax', models.CharField(max_length=50, null=True)),
                ('request_form', models.URLField(null=True)),
                ('website', models.URLField(null=True)),
                ('emails', models.CharField(max_length=250, null=True)),
                ('contact', models.TextField(null=True)),
                ('contact_phone', models.CharField(max_length=50, null=True)),
                ('public_liaison', models.TextField(null=True)),
                ('notes', models.TextField(null=True)),
                ('agency', models.ForeignKey(to='foia_hub.Agency')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Requester',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='office',
            unique_together=set([('slug', 'agency')]),
        ),
        migrations.AddField(
            model_name='foiarequest',
            name='office',
            field=models.ForeignKey(to='foia_hub.Office'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foiarequest',
            name='requester',
            field=models.ForeignKey(to='foia_hub.Requester'),
            preserve_default=True,
        ),
    ]
