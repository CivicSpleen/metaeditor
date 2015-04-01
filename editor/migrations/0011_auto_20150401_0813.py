# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0010_auto_20150319_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='abbreviation',
            field=models.CharField(help_text=b'A common abbreviation for the name of the source, such as "HHS".', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='about',
            field=models.TextField(help_text=b'Freeform text, paragraph length.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='domain',
            field=models.CharField(help_text=b'A short string, by default derived from the Home page url.', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
