# Generated by Django 2.0 on 2018-02-08 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0030_auto_20180208_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestedvideo',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='suggestedvideo',
            name='video_id',
            field=models.CharField(blank=True, editable=False, max_length=12),
        ),
    ]