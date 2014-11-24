# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0015_adding_stats_obj'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadingRoomUrls',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('link_text', models.CharField(max_length=512, help_text='This is the text associated with the reading room URL. ')),
                ('url', models.URLField(null=True, help_text="The URL to an agency's reading room.")),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='readingroomurls',
            unique_together=set([('link_text', 'url')]),
        ),
        migrations.RemoveField(
            model_name='agency',
            name='reading_room_url',
        ),
        migrations.RemoveField(
            model_name='office',
            name='reading_room_url',
        ),
        migrations.AddField(
            model_name='agency',
            name='reading_room_urls',
            field=models.ManyToManyField(to='foia_hub.ReadingRoomUrls', related_name='foia_hub_agency_related'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='office',
            name='reading_room_urls',
            field=models.ManyToManyField(to='foia_hub.ReadingRoomUrls', related_name='foia_hub_office_related'),
            preserve_default=True,
        ),
    ]
