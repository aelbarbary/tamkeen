# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-12 05:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0041_auto_20170307_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='youth',
            name='user_name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
