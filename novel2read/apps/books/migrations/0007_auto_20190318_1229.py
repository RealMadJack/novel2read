# Generated by Django 2.0.13 on 2019-03-18 09:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20190318_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='volumes',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.SmallIntegerField(default=0), default=list, size=None), blank=True, default=list, size=None),
        ),
    ]