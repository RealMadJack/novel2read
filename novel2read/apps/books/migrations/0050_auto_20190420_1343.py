# Generated by Django 2.1.7 on 2019-04-20 10:43

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0049_auto_20190418_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='volumes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.SmallIntegerField(default=1), blank=True, default=list, size=None),
        ),
    ]
