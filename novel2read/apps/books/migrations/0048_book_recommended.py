# Generated by Django 2.1.7 on 2019-04-16 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0047_auto_20190416_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='recommended',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
