# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import editor.models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0008_auto_20150315_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 16, 14, 54, 3, 122690, tzinfo=utc), help_text=b'Creation date and time', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documentfile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 16, 14, 54, 14, 307008, tzinfo=utc), help_text=b'Creation date and time', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datafile',
            name='f',
            field=models.FileField(upload_to=editor.models._get_upload_path),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datafile',
            name='file_format',
            field=models.ForeignKey(blank=True, to='editor.Format', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='f',
            field=models.FileField(upload_to=editor.models._get_upload_path),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='file_format',
            field=models.ForeignKey(blank=True, to='editor.Format', null=True),
            preserve_default=True,
        ),
    ]
