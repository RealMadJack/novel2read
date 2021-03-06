# Generated by Django 2.1.7 on 2019-05-11 08:24

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20190508_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookChapterReplace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('replace', models.CharField(default='', max_length=355, verbose_name='Replace')),
                ('replace_to', models.CharField(blank=True, default='', max_length=355, verbose_name='Replace to')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
