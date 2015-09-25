# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=48, unique=True, null=True)),
                ('descripcion', models.CharField(max_length=100, null=True)),
                ('punitario', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('pmayoreo', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('inventario', models.BooleanField(default=False)),
                ('cantidad', models.IntegerField(null=True)),
                ('minimo', models.IntegerField(null=True)),
            ],
        ),
    ]
