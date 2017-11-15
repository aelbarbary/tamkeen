# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-07 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0018_inquiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='email',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='text',
            field=models.TextField(verbose_name='Inquiry'),
        ),
        migrations.AlterField(
            model_name='newmemberrequest',
            name='whats_app',
            field=models.CharField(blank=True, max_length=20, verbose_name='Phone Number'),
        ),
    ]