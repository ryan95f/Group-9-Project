# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('is_readonly', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveSmallIntegerField(null=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('author', models.CharField(max_length=100, null=True, blank=True)),
                ('version', models.CharField(max_length=100, null=True, blank=True)),
                ('new_commands', models.CharField(max_length=5000, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_class', models.CharField(max_length=10)),
                ('node_type', models.CharField(max_length=10)),
                ('number', models.PositiveSmallIntegerField(null=True)),
                ('title', models.CharField(max_length=100, null=True)),
                ('is_readonly', models.BooleanField(default=False)),
                ('text', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to=b'figure_images')),
                ('node_id', models.PositiveSmallIntegerField()),
                ('mpath', models.CharField(max_length=100, null=True)),
                ('label', models.CharField(max_length=100, null=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='core.BookNode', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=100)),
                ('mpath', models.CharField(max_length=1000)),
                ('book', models.ForeignKey(to='core.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.CharField(max_length=6, choices=[(b'2014-15', b'2014-15'), (b'2015-16', b'2015-16'), (b'2016-17', b'2016-17')])),
                ('code', models.CharField(max_length=7, choices=[(b'MA0000', b'MA0000'), (b'MA0003', b'MA0003'), (b'MA1234', b'MA1234'), (b'MA1501', b'MA1501')])),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('twitter_widget_id', models.CharField(max_length=1024, null=True, blank=True)),
                ('students', models.ManyToManyField(related_name='module_students', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('teacher', models.ForeignKey(related_name='module_teacher', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SingleChoiceAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_readonly', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('choice', models.ForeignKey(related_name='mcanswer_choice', to='core.BookNode')),
                ('question', models.ForeignKey(to='core.BookNode')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_readonly', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(to='core.BookNode')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.AddField(
            model_name='book',
            name='module',
            field=models.ForeignKey(related_name='book_module', blank=True, to='core.Module', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='tree',
            field=models.ForeignKey(related_name='book_tree', to='core.BookNode', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='core.BookNode'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
