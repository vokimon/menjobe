# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menjobe', '0008_auto_20140829_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='retailpoint',
            name='description',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
