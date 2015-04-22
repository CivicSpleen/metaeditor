# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0016_dataset_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='coverage',
            field=models.CharField(max_length=50, verbose_name=b'Geo Coverage'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='region',
            field=models.CharField(max_length=100, verbose_name=b'Geo Grain', choices=[(b'1D00000000000', b'Block'), (b'2q0000000000', b'Blockgroup'), (b'0Y0000000', b'Cosub'), (b'0O0000', b'County'), (b'0u0', b'Division'), (b'2A000000', b'Place'), (b'0k0', b'Region'), (b'fk000000', b'Sdelm'), (b'fu000000', b'Sdsec'), (b'fE000000', b'Sduni'), (b'0E00', b'State'), (b'2g000000000', b'Tract'), (b'6s0000', b'Ua'), (b'dS0000', b'Zcta'), (b'jm0000', b'Zip')]),
            preserve_default=True,
        ),
    ]
