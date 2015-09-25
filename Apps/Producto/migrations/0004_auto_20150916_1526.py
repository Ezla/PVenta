# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0003_auto_20150908_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='code39',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.CharField(max_length=48, unique=True, null=True, blank=True),
        ),
    ]
