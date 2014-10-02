# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0005_auto_20141001_1652'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agency',
            old_name='public_liason_email',
            new_name='public_liaison_email',
        ),
        migrations.RenameField(
            model_name='agency',
            old_name='public_liason_name',
            new_name='public_liaison_name',
        ),
        migrations.RenameField(
            model_name='agency',
            old_name='public_liason_phone',
            new_name='public_liaison_phone',
        ),
        migrations.RenameField(
            model_name='office',
            old_name='public_liason_email',
            new_name='public_liaison_email',
        ),
        migrations.RenameField(
            model_name='office',
            old_name='public_liason_name',
            new_name='public_liaison_name',
        ),
        migrations.RenameField(
            model_name='office',
            old_name='public_liason_phone',
            new_name='public_liaison_phone',
        ),
    ]
