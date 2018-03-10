# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import Apps.Venta.models


class Migration(migrations.Migration):

    dependencies = [
        ('Venta', '0002_auto_20150622_0111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descuento', models.PositiveSmallIntegerField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='cuenta',
            name='descuento',
            field=models.ForeignKey(default=Apps.Venta.models.default_descuento, on_delete=models.CASCADE,
                                    to='Venta.Descuento'),
        ),
    ]
