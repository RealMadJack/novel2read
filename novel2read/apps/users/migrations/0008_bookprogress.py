# Generated by Django 2.0.13 on 2019-03-23 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0026_remove_book_chapters_max'),
        ('users', '0007_auto_20190323_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_id', models.IntegerField(blank=True, default=0, null=True, verbose_name='Chapter ID')),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
                ('library', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Library')),
            ],
            options={
                'verbose_name': 'Book Progress',
                'verbose_name_plural': 'Book Progresses',
            },
        ),
    ]
