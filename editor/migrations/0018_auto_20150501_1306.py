# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0017_auto_20150422_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='vid',
            field=models.CharField(help_text=b'An unique number from ambry.', max_length=20, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='region',
            field=models.CharField(max_length=100, verbose_name=b'Geo Grain', choices=[(b'1DZZZZZZZZZZZ', b'Block'), (b'2qZZZZZZZZZZ', b'Blockgroup'), (b'0YZZZZZZZ', b'Cosub'), (b'0OZZZZ', b'County'), (b'0uZ', b'Division'), (b'2AZZZZZZ', b'Place'), (b'0kZ', b'Region'), (b'fkZZZZZZ', b'Sdelm'), (b'fuZZZZZZ', b'Sdsec'), (b'fEZZZZZZ', b'Sduni'), (b'0EZZ', b'State'), (b'2gZZZZZZZZZ', b'Tract'), (b'6sZZZZ', b'Ua'), (b'0a', b'Us'), (b'dSZZZZ', b'Zcta'), (b'jmZZZZ', b'Zip')]),
            preserve_default=True,
        ),
    ]
