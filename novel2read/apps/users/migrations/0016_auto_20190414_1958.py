# Generated by Django 2.1.7 on 2019-04-14 16:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20190411_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='premium',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='premium_expire',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]