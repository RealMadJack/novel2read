# Generated by Django 2.1.7 on 2019-04-15 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0032_book_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_id_wn',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='WN book id'),
        ),
    ]
