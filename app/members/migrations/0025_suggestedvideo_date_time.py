from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('members', '0024_auto_20171117_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestedvideo',
            name='date_time',
            field=models.DateTimeField(default='2017-11-11'),
            preserve_default=False,
        ),
    ]
