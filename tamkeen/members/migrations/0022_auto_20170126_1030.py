# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-26 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0021_event_registeration_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youth',
            name='rank',
            field=models.IntegerField(default=1),
        ),
    ]
