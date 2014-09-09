# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menjobe', '0009_retailpoint_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='retailpoint',
            name='address',
            field=models.TextField(default=None, null=True),
            preserve_default=True,
        ),
    ]
