# Generated by Django 2.0.13 on 2019-03-20 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0022_auto_20190320_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='locked_wn',
        ),
    ]
