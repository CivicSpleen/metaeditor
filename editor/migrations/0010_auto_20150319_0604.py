# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0009_auto_20150316_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datafile',
            name='f',
        ),
        migrations.RemoveField(
            model_name='documentfile',
            name='f',
        ),
        migrations.AddField(
            model_name='datafile',
            name='name',
            field=models.CharField(default='?', max_length=200, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datafile',
            name='url',
            field=models.URLField(default='?', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documentfile',
            name='name',
            field=models.CharField(default='?', max_length=200, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documentfile',
            name='url',
            field=models.URLField(default='?', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datafile',
            name='dataset',
            field=models.ForeignKey(default=1, to='editor.Dataset'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datafile',
            name='file_format',
            field=models.ForeignKey(default=1, to='editor.Format'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='dataset',
            field=models.ForeignKey(default=1, to='editor.Dataset'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='file_format',
            field=models.ForeignKey(default=1, to='editor.Format'),
            preserve_default=False,
        ),
    ]
