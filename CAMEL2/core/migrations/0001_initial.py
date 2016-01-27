# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('year', models.CharField(max_length=6, choices=[('2014-15', '2014-15'), ('2015-16', '2015-16'), ('2016-17', '2016-17')])),
                ('code', models.CharField(max_length=7, choices=[('MA0000', 'MA0000'), ('MA0003', 'MA0003'), ('MA1234', 'MA1234'), ('MA1501', 'MA1501')])),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('twitter_widget_id', models.CharField(max_length=1024, null=True, blank=True)),
                ('students', models.ManyToManyField(related_name='module_students', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='module_teacher', null=True)),
            ],
        ),
    ]
