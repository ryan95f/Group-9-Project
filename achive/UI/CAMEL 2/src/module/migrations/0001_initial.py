# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('latexbook', '0002_auto_20160131_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('books', models.ManyToManyField(to='latexbook.Book')),
            ],
        ),
    ]
