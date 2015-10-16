# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150604_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='module',
            field=models.ForeignKey(related_name='book_set', blank=True, to='core.Module', null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='students',
            field=models.ManyToManyField(related_name='module_students', to=settings.AUTH_USER_MODEL),
        ),
    ]
