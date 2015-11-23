# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import Apps.Perfil.models


class Migration(migrations.Migration):

    dependencies = [
        ('Perfil', '0004_auto_20151122_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=Apps.Perfil.models.url, blank=True),
        ),
    ]
