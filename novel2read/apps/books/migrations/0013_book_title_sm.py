# Generated by Django 2.0.13 on 2019-03-19 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_book_chapters_release'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='title_sm',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Title short'),
        ),
    ]