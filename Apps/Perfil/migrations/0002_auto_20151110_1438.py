# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Apps.Perfil.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Perfil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plantilla', models.IntegerField(default=1, choices=[(1, b'Predeterminado'), (2, b'Clasico')])),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to=Apps.Perfil.models.url),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name='profile', on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='config',
            field=models.OneToOneField(null=True, on_delete=models.CASCADE, to='Perfil.UserConfig'),
        ),
    ]
