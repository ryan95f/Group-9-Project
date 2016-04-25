# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='year',
            field=models.CharField(max_length=6, choices=[('2014-15', '2014-15'), ('2015-16', '2015-16'), ('2016-17', '2016-17'), ('2017-18', '2017-18')], default=datetime.datetime(2016, 2, 26, 19, 13, 42, 987317, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
