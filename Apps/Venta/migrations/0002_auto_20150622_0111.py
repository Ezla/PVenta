# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Venta', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cuenta',
            old_name='fecha',
            new_name='modificado',
        ),
        migrations.AddField(
            model_name='cuenta',
            name='creado',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
