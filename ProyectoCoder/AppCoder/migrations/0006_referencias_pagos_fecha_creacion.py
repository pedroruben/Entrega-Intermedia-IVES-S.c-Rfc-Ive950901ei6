# Generated by Django 4.1.3 on 2022-11-26 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0005_alter_alumno_matricula_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='referencias_pagos',
            name='fecha_creacion',
            field=models.DateField(null=True),
        ),
    ]
