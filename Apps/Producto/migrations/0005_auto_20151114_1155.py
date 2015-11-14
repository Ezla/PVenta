# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0004_auto_20150916_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='vunidad',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(default='acyualizame', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producto',
            name='pmayoreo',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producto',
            name='punitario',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=2),
            preserve_default=False,
        ),
    ]
