# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0007_auto_20150309_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafile',
            name='dataset',
            field=models.ForeignKey(blank=True, to='editor.Dataset', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='dataset',
            field=models.ForeignKey(blank=True, to='editor.Dataset', null=True),
            preserve_default=True,
        ),
    ]
