# Generated by Django 2.1.7 on 2019-04-16 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0037_auto_20190415_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='poster',
            field=models.ImageField(blank=True, default='/static/images/default-612.jpg', null=True, upload_to='posters/', verbose_name='Poster'),
        ),
    ]
