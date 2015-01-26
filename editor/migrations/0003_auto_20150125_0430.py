# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from editor.models import Source, Category, Format

# add root data for Source and Category model
def add_root_data(apps, schema_editor):
    cat = Category(name ="root", parent=None)
    cat.save()

    source = Source(
        name = "root",
        abbreviation = "root",
        domain = "",
        homepage = "",
        about = "",
        parent = None,
    )
    source.save()
    source.categories.add(cat)

    f = Format(name ="root", parent=None)
    f.save()

def revert(apps, schema_editor):
    for source in Source.objects.all():
        source.delete()
    for category in Category.objects.all():
        category.delete()
    for f in Format.objects.all():
        f.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0002_auto_20150124_1912'),
    ]

    operations = [
        migrations.RunPython(add_root_data, reverse_code=revert),
    ]

