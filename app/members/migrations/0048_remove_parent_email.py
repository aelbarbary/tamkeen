# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-05 22:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0047_remove_child_interests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='email',
        ),
    ]