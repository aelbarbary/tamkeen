# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-24 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0036_auto_20170224_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionanswer',
            name='score',
            field=models.IntegerField(null=True),
        ),
    ]
