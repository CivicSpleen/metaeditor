# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0006_auto_20150309_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='source',
            field=models.ForeignKey(default=1, to='editor.Source', help_text=b'Source of the dataset.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datafile',
            name='f',
            field=models.FileField(upload_to=b'uploads'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='f',
            field=models.FileField(upload_to=b'uploads'),
            preserve_default=True,
        ),
    ]
