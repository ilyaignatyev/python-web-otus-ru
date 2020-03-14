# Generated by Django 3.0.3 on 2020-03-11 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_app', '0005_auto_20200312_0248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='admins',
            field=models.ManyToManyField(blank=True, through='education_app.CourseAdmin', to='education_app.Administrator', verbose_name='Администраторы'),
        ),
    ]
