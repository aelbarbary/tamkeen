# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-19 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_profile_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.CharField(default='TAMKEENER', max_length=100),
        ),
    ]
