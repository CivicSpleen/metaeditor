# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0005_auto_20150222_0508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='coverage_name',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='coverage_type',
        ),
        migrations.AddField(
            model_name='dataset',
            name='coverage',
            field=models.CharField(default='?', max_length=50, choices=[(b'national', b'National'), (b'state', b'State'), (b'county', b'County'), (b'sub-county', b'Sub county')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataset',
            name='region',
            field=models.CharField(default='?', max_length=100, choices=[(b'state', b'State'), (b'state_and_county', b'State and county')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text=b'The name of the category', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, to='editor.Category', help_text=b'A link to another category', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='categories',
            field=models.ManyToManyField(help_text=b'Multiple links to names of categories.', to='editor.Category'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='contacts',
            field=models.TextField(help_text=b'Freeform text of people to email or call about the dataset. '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='download_page',
            field=models.URLField(help_text=b'URL of a web page where dataset files can be downloaded.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='end_year',
            field=models.IntegerField(help_text=b'The last year for which the dataset has data.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='entry_time_minutes',
            field=models.IntegerField(help_text=b'A record of how long the user spent creating the record.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='formats',
            field=models.ManyToManyField(help_text=b'Collection of Formats associated with this dataset.', to='editor.Format'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='page',
            field=models.URLField(help_text=b'URL of a web page about the dataset.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='start_year',
            field=models.IntegerField(help_text=b'The first year for which the dataset has data.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='title',
            field=models.CharField(help_text=b'The title of the dataset.', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='user',
            field=models.ForeignKey(help_text=b'Link to the user that edited this dataset. ', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='variant',
            field=models.CharField(help_text=b'Distinguished this dataset from similar datasets.', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='format',
            name='name',
            field=models.CharField(help_text=b'The name of the format.', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='format',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, to='editor.Format', help_text=b'A link to another format.', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='abbreviation',
            field=models.CharField(help_text=b'A common abbreviation for the name of the source, such as "HHS".', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='about',
            field=models.TextField(help_text=b'Freeform text, paragraph length.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='categories',
            field=models.ManyToManyField(help_text=b'Multiple links to names of categories.', to='editor.Category'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='domain',
            field=models.CharField(help_text=b'A short string, by default derived from the Home page url.', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='homepage',
            field=models.URLField(help_text=b'URL of the home page for the organization.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.CharField(help_text=b'Formal name of the source. such as "Department of Health and Human Services".', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, to='editor.Source', help_text=b'A link to another source.', null=True),
            preserve_default=True,
        ),
    ]
