# Generated by Django 2.0.6 on 2018-09-09 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(max_length=8, null=True),
        ),
    ]