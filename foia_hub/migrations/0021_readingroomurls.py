# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0020_delete_readingroomurls'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadingRoomUrls',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('link_text', models.CharField(max_length=512, help_text='This is the text associated with the reading room URL. ')),
                ('url', models.URLField(null=True, help_text="The URL to an agency's reading room.")),
                ('agency', models.ForeignKey(to='foia_hub.Agency')),
                ('office', models.ForeignKey(to='foia_hub.Office', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
