# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0011_auto_20150401_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='categories',
            field=models.ManyToManyField(help_text=b'Multiple links to names of categories.', to='editor.Category', null=True, blank=True),
            preserve_default=True,
        ),
    ]
