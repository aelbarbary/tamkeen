# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-17 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0044_auto_20170313_0502'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ImageField(default='no-img.jpg', upload_to='question'),
        ),
    ]