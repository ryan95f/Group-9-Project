# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='homework_node',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='singlechoiceanswer',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='singlechoiceanswer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='singlechoiceanswer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='user',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='SingleChoiceAnswer',
        ),
        migrations.DeleteModel(
            name='Submission',
        ),
    ]
