# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0003_auto_20160226_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='code',
            field=models.CharField(primary_key=True, serialize=False, max_length=7),
        ),
        migrations.AlterField(
            model_name='module',
            name='year',
            field=models.CharField(max_length=7, choices=[('2014-15', '2014-15'), ('2015-16', '2015-16'), ('2016-17', '2016-17'), ('2017-18', '2017-18')]),
        ),
    ]
