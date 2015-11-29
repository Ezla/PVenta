# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0005_auto_20151114_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='modificado',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 29, 22, 43, 12, 636000, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
