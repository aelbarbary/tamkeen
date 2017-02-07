# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 05:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0019_auto_20170119_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(default='pic_folder/no-img.jpg', upload_to='event'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='image',
            field=models.ImageField(default='pic_folder/no-img.jpg', upload_to='volunteer'),
        ),
        migrations.AlterField(
            model_name='youth',
            name='image',
            field=models.ImageField(default='pic_folder/no-img.jpg', upload_to='youth'),
        ),
    ]