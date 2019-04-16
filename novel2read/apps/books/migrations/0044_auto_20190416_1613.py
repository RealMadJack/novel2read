# Generated by Django 2.1.7 on 2019-04-16 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0043_auto_20190416_1411'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='visited',
            new_name='visit',
        ),
        migrations.RemoveField(
            model_name='book',
            name='visited_id',
        ),
        migrations.AddField(
            model_name='book',
            name='visit_id',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Visit id'),
        ),
    ]
