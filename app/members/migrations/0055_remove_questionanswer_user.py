# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 23:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0054_auto_20170918_2239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionanswer',
            name='user',
        ),
    ]
