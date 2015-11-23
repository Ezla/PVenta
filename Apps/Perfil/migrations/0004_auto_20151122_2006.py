# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import Apps.Perfil.models


class Migration(migrations.Migration):

    dependencies = [
        ('Perfil', '0003_auto_20151110_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to=Apps.Perfil.models.url, blank=True),
        ),
    ]
