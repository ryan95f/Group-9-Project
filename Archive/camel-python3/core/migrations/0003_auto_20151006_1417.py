# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150604_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='module',
            field=models.ForeignKey(blank=True, to='core.Module', related_name='book_set', null=True),
        ),
        migrations.AlterField(
            model_name='booknode',
            name='image',
            field=models.ImageField(upload_to='figure_images', null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='code',
            field=models.CharField(max_length=7, choices=[('MA0000', 'MA0000'), ('MA0003', 'MA0003'), ('MA1234', 'MA1234'), ('MA1501', 'MA1501')]),
        ),
        migrations.AlterField(
            model_name='module',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='module_students'),
        ),
        migrations.AlterField(
            model_name='module',
            name='year',
            field=models.CharField(max_length=6, choices=[('2014-15', '2014-15'), ('2015-16', '2015-16'), ('2016-17', '2016-17')]),
        ),
    ]
