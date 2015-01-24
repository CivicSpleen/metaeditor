# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(to='editor.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('f', models.FileField(upload_to=b'')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('variant', models.CharField(max_length=100)),
                ('start_year', models.IntegerField()),
                ('end_year', models.IntegerField()),
                ('coverage_type', models.CharField(max_length=50)),
                ('coverage_name', models.CharField(max_length=100)),
                ('page', models.URLField()),
                ('download_page', models.URLField()),
                ('contacts', models.TextField()),
                ('is_complex', models.BooleanField()),
                ('is_reviewed', models.BooleanField()),
                ('has_restricted_version', models.BooleanField()),
                ('has_restrictive_licensing', models.BooleanField()),
                ('has_direct_public_download', models.BooleanField()),
                ('entry_time_minutes', models.IntegerField()),
                ('categories', models.ManyToManyField(to='editor.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('f', models.FileField(upload_to=b'')),
                ('dataset', models.ForeignKey(to='editor.Dataset')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(to='editor.Format', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('abbreviation', models.CharField(max_length=50)),
                ('domain', models.CharField(max_length=50)),
                ('homepage', models.URLField()),
                ('about', models.TextField()),
                ('categories', models.ManyToManyField(to='editor.Category')),
                ('parent', models.ForeignKey(to='editor.Source', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='documentfile',
            name='file_format',
            field=models.ForeignKey(to='editor.Format'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dataset',
            name='formats',
            field=models.ManyToManyField(to='editor.Format'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dataset',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datafile',
            name='dataset',
            field=models.ForeignKey(to='editor.Dataset'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datafile',
            name='file_format',
            field=models.ForeignKey(to='editor.Format'),
            preserve_default=True,
        ),
    ]
