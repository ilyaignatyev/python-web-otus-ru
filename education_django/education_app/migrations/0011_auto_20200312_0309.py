# Generated by Django 3.0.3 on 2020-03-12 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_app', '0010_auto_20200312_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseadmin',
            name='start',
            field=models.DateField(verbose_name='Дата начала'),
        ),
    ]
