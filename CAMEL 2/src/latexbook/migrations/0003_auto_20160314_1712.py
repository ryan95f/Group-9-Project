# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-14 17:12
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('latexbook', '0002_auto_20160131_1200'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='booknode',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
