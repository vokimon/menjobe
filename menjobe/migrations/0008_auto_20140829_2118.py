# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menjobe', '0007_retailpoint_retailedproducts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retailpoint',
            name='retailedProducts',
            field=models.ManyToManyField(to='menjobe.Product', blank=True),
        ),
    ]
