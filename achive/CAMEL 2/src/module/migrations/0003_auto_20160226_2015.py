# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0002_module_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='code',
            field=models.CharField(choices=[('MA0000', 'MA0000'), ('MA0003', 'MA0003'), ('MA1234', 'MA1234'), ('MA1501', 'MA1501')], serialize=False, max_length=6, primary_key=True),
        ),
    ]
