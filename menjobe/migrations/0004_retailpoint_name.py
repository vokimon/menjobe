# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menjobe', '0003_retailpoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='retailpoint',
            name='name',
            field=models.CharField(max_length=200, default=None),
            preserve_default=True,
        ),
    ]
