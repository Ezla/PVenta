# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='cantidad',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='minimo',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
