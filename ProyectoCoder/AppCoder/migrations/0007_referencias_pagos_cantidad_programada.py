# Generated by Django 4.1.3 on 2022-11-27 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0006_referencias_pagos_fecha_creacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='referencias_pagos',
            name='cantidad_programada',
            field=models.IntegerField(null=True),
        ),
    ]
