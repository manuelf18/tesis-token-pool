# Generated by Django 2.2.2 on 2019-09-17 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0005_auto_20190726_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('active', models.BooleanField(default=True, verbose_name='activo')),
                ('address', models.CharField(default='', max_length=50, verbose_name='Dirección')),
                ('transaction_type', models.IntegerField(choices=[(0, 0), (1, 1)])),
                ('amount', models.DecimalField(decimal_places=4, max_digits=9, verbose_name='Cantidad de tokens')),
                ('value', models.DecimalField(decimal_places=4, max_digits=9, verbose_name='Valor de los tokens')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
