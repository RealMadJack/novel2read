# Generated by Django 2.0.13 on 2019-03-20 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0020_auto_20190320_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='c_id',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Chapter ID'),
        ),
    ]
