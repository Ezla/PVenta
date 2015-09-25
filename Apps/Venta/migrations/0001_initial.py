# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tiket', models.CharField(max_length=30, null=True)),
                ('total', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('efectivo', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('cambio', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('fecha', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=48, null=True)),
                ('nombre', models.CharField(max_length=100, null=True)),
                ('descuento', models.BooleanField(default=False)),
                ('precio', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('cantidad', models.IntegerField(null=True)),
                ('subtotal', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('cuenta', models.ForeignKey(to='Venta.Cuenta', null=True)),
            ],
        ),
    ]
