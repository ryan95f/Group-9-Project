# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 21:40
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('latexbook', '0007_auto_20160329_1703'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='booknode',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
