# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('position', models.IntegerField()),
                ('node_type', models.CharField(max_length=50)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('title', models.CharField(max_length=64)),
                ('author', models.CharField(max_length=64)),
                ('book_root_node', models.OneToOneField(related_name='book', serialize=False, primary_key=True, to='latexbook.BookNode')),
                ('module_codes', models.ManyToManyField(to='latexbook.Module')),
            ],
        ),
        migrations.CreateModel(
            name='TextNode',
            fields=[
                ('book_node', models.OneToOneField(related_name='text_node', serialize=False, primary_key=True, to='latexbook.BookNode')),
                ('content', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='booknode',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', to='latexbook.BookNode', blank=True, null=True),
        ),
    ]
