# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-18 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0033_auto_20170218_2216'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Competition',
        ),
        migrations.AlterField(
            model_name='event',
            name='gender',
            field=models.BooleanField(default=False, verbose_name='Gender:'),
        ),
    ]