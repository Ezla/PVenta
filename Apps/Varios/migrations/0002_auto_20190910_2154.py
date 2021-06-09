# Generated by Django 2.0.6 on 2019-09-11 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Varios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listed',
            name='provider',
            field=models.CharField(choices=[('1', 'SUN RISE'), ('2', 'RAF')], default=1, max_length=1, verbose_name='Proveedor del producto'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listed',
            name='reference_number',
            field=models.CharField(default=0, max_length=8, verbose_name='Número de referencia'),
            preserve_default=False,
        ),
    ]
