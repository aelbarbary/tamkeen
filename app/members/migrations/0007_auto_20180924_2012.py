# Generated by Django 2.0.6 on 2018-09-25 03:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_auto_20180924_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='people',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=10), default=list, null=True, size=10),
        ),
    ]
