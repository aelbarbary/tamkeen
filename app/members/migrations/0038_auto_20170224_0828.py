# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-24 08:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0037_auto_20170224_0818'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionanswer',
            old_name='event',
            new_name='question',
        ),
    ]