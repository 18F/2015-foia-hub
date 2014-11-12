# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0013_add_request_relationship_to_agency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('year', models.PositiveSmallIntegerField()),
                ('stat_type', models.CharField(max_length=1, choices=[('S', 'simple'), ('C', 'complex'), ('E', 'expedited')])),
                ('average', models.FloatField(null=True, blank=True)),
                ('median', models.FloatField(null=True, blank=True)),
                ('high', models.FloatField(null=True, blank=True)),
                ('low', models.FloatField(null=True, blank=True)),
                ('agency', models.ForeignKey(to='foia_hub.Agency')),
                ('office', models.ForeignKey(null=True, blank=True, to='foia_hub.Office')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='stats',
            unique_together=set([('agency', 'office', 'year', 'stat_type')]),
        )
    ]
