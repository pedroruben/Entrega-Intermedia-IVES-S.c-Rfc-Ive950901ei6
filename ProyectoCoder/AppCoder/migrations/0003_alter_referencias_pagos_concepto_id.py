# Generated by Django 4.1.3 on 2022-11-23 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0002_referencias_pagos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referencias_pagos',
            name='concepto_id',
            field=models.CharField(max_length=100),
        ),
    ]