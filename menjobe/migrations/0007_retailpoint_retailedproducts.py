# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menjobe', '0006_auto_20140829_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='retailpoint',
            name='retailedProducts',
            field=models.ManyToManyField(to='menjobe.Product'),
            preserve_default=True,
        ),
    ]
