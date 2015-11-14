# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Perfil', '0002_auto_20151110_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='config',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plantilla',
            field=models.IntegerField(default=1, choices=[(1, b'Predeterminado'), (2, b'Clasico')]),
        ),
        migrations.DeleteModel(
            name='UserConfig',
        ),
    ]
