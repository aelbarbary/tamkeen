# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 03:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20170117_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youth',
            name='image',
            field=models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='pic_folder/'),
        ),
    ]
