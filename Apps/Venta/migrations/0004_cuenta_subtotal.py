# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venta', '0003_auto_20160820_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuenta',
            name='subtotal',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2),
        ),
    ]
