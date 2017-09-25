# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-25 21:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0055_remove_questionanswer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=2000)),
                ('date_time', models.DateTimeField()),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
            ],
        ),
        migrations.RemoveField(
            model_name='child',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='eventregistered',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventregistered',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='user_ptr',
        ),
        migrations.RemoveField(
            model_name='questionanswer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='closed',
        ),
        migrations.DeleteModel(
            name='Child',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='EventRegistered',
        ),
        migrations.DeleteModel(
            name='Parent',
        ),
        migrations.DeleteModel(
            name='QuestionAnswer',
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='members.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='members.Quiz'),
            preserve_default=False,
        ),
    ]
