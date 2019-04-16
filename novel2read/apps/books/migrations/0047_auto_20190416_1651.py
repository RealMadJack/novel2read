# Generated by Django 2.1.7 on 2019-04-16 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0046_book_revisited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='revisit',
            field=models.CharField(blank=True, choices=[('webnovel', 'Webnovel'), ('boxnovel', 'Boxnovel'), ('wuxiaworld', 'WuxiaWorld'), ('gravitytails', 'GravityTails'), ('lnmtl', 'LNMTL')], default='webnovel', max_length=55),
        ),
        migrations.AlterField(
            model_name='book',
            name='visit',
            field=models.CharField(blank=True, choices=[('webnovel', 'Webnovel'), ('boxnovel', 'Boxnovel'), ('wuxiaworld', 'WuxiaWorld'), ('gravitytails', 'GravityTails'), ('lnmtl', 'LNMTL')], default='webnovel', max_length=55),
        ),
    ]