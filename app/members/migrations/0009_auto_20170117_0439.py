# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 04:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20170117_0427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youth',
            name='image',
            field=models.ImageField(default='static/pic_folder/no-img.jpg', upload_to='/pic_folder/'),
        ),
    ]