# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0004_auto_20150216_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='format',
            name='level',
            field=models.PositiveIntegerField(default='0', editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='format',
            name='lft',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='format',
            name='rght',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='format',
            name='tree_id',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='source',
            name='level',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='source',
            name='lft',
            field=models.PositiveIntegerField(default='0', editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='source',
            name='rght',
            field=models.PositiveIntegerField(default='0', editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='source',
            name='tree_id',
            field=models.PositiveIntegerField(default='0', editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='format',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, to='editor.Format', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, to='editor.Source', null=True),
            preserve_default=True,
        ),
    ]
