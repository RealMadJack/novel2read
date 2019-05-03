# Generated by Django 2.1.7 on 2019-05-03 14:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_bookprogress_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookprogress',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bookprogress',
            name='book',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='books.Book'),
        ),
    ]
