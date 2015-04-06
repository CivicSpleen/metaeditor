# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0012_auto_20150401_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='contacts',
            field=models.TextField(help_text=b'Freeform text of people to email or call about the dataset. ', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='download_page',
            field=models.URLField(help_text=b'URL of a web page where dataset files can be downloaded.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='variant',
            field=models.CharField(help_text=b'Distinguished this dataset from similar datasets.', max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
