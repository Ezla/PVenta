# Generated by Django 2.0.6 on 2018-07-15 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Venta', '0004_cuenta_subtotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.PositiveSmallIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SalesAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(max_length=30, blank=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cash', models.DecimalField(decimal_places=2, max_digits=10)),
                ('change_due', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Venta.Discount')),
            ],
        ),
        migrations.CreateModel(
            name='SalesProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=48)),
                ('name', models.CharField(max_length=100)),
                ('with_discount', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.IntegerField()),
                ('sales_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='Venta.SalesAccount')),
            ],
        ),
        migrations.RemoveField(
            model_name='cuenta',
            name='descuento',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='cuenta',
        ),
        migrations.DeleteModel(
            name='Cuenta',
        ),
        migrations.DeleteModel(
            name='Descuento',
        ),
        migrations.DeleteModel(
            name='Venta',
        ),
    ]
