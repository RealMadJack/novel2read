# Generated by Django 2.1.7 on 2019-04-16 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0039_auto_20190416_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='poster_url',
        ),
    ]