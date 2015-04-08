# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('editor', '0013_auto_20150406_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='created_by',
            field=models.ForeignKey(related_name='created_sources', blank=True, to=settings.AUTH_USER_MODEL, help_text=b'User who created that source.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_sources', blank=True, to=settings.AUTH_USER_MODEL, help_text=b'User who last edited that source.', null=True),
            preserve_default=True,
        ),
    ]
