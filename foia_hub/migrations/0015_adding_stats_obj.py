# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0014_freeze_contact_info_on_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('year', models.PositiveSmallIntegerField()),
                ('stat_type', models.CharField(choices=[('S', 'simple'), ('C', 'complex')], max_length=1)),
                ('median', models.FloatField(blank=True, null=True)),
                ('agency', models.ForeignKey(to='foia_hub.Agency')),
                ('office', models.ForeignKey(blank=True, to='foia_hub.Office', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='stats',
            unique_together=set([('agency', 'office', 'year', 'stat_type')]),
        ),
        migrations.AlterField(
            model_name='foiarequest',
            name='emails',
            field=jsonfield.fields.JSONField(null=True),
        ),
    ]
