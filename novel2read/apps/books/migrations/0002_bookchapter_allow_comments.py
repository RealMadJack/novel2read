# Generated by Django 2.1.7 on 2019-05-05 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookchapter',
            name='allow_comments',
            field=models.BooleanField(default=True, verbose_name='allow comments'),
        ),
    ]