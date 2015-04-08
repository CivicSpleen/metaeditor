# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0014_auto_20150407_0801'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name of the extension.', max_length=20, db_index=True)),
                ('format', models.ForeignKey(to='editor.Format')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='extension',
            unique_together=set([('name', 'format')]),
        ),
    ]
