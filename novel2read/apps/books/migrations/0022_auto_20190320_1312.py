# Generated by Django 2.0.13 on 2019-03-20 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0021_book_c_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='c_id',
        ),
        migrations.AddField(
            model_name='bookchapter',
            name='c_id',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Chapter ID'),
        ),
    ]