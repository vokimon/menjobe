# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menjobe', '0005_auto_20140829_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retailpoint',
            name='name',
            field=models.CharField(max_length=200, unique=True, default=None),
        ),
    ]
