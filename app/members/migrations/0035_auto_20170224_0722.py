# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-24 07:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0034_auto_20170218_2247'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=2000)),
                ('date_time', models.DateTimeField()),
                ('closed', models.BooleanField(verbose_name='closed:')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=2000)),
                ('name', models.CharField(max_length=2000)),
                ('date_time', models.DateTimeField()),
                ('score', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='members.Question')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='gender',
            field=models.BooleanField(verbose_name='Gender:'),
        ),
    ]
