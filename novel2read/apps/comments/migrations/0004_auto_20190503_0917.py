# Generated by Django 2.1.7 on 2019-05-03 06:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0003_set_site_domain_and_name'),
        ('django_comments_xtd', '0006_auto_20181204_0948'),
        ('django_comments', '0003_add_submit_date_index'),
        ('comments', '0003_auto_20190503_0915'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BasicComment',
            new_name='CustomComment',
        ),
    ]