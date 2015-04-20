# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0015_auto_20150408_0645'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='about',
            field=models.TextField(help_text=b'Freeform text about the dataset.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
