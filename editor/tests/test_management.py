# -*- coding: utf-8 -*-
import os
import csv

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from editor.models import Source, Category, Format
from editor.tests.factories import SourceFactory, CategoryFactory, FormatFactory


class LoadSourcesTest(TestCase):

    @classmethod
    def setUpClass(cls):

        # cache sources.csv rows for all tests
        sources = os.path.join(
            settings.BASE_DIR, '../', 'editor', 'data', 'sources.csv')

        cls._csv_rows = []
        with open(sources) as csvfile:
            reader = csv.DictReader(csvfile)
            for node in reader:
                cls._csv_rows.append(node)

    def test_raises_command_error_if_sources_exist(self):
        SourceFactory()
        self.assertRaises(CommandError, call_command, 'load_sources', verbosity=0)

    def _assert_all_nodes_imported(self):

        self.assertEqual(
            Source.objects.all().count(),
            len(self._csv_rows))
        for node in self._csv_rows:
            node_instance = Source.objects.get(
                id=long(node['id']),
                name=node['name'],
                abbreviation=node['abbreviation'],
                domain=node['domain'],
                homepage=node['homepage'],
                about=node['about'])

            if node['parent_id']:
                self.assertEquals(node_instance.parent.id, long(node['parent_id']))
            else:
                # root node
                self.assertIsNone(node_instance.parent)

    def test_deletes_existing_and_creates_new_nodes(self):
        s1 = SourceFactory()
        s2 = SourceFactory()
        self.assertEqual(Source.objects.all().count(), 2)
        call_command('load_sources', verbosity=0, delete=True)
        self.assertEquals(Source.objects.filter(name=s1.name).count(), 0)
        self.assertEquals(Source.objects.filter(name=s2.name).count(), 0)
        self._assert_all_nodes_imported()

    def test_saves_all_nodes(self):
        self.assertEqual(Source.objects.all().count(), 0)
        call_command('load_sources', verbosity=0)
        self._assert_all_nodes_imported()


class CreateGlobalRootsTest(TestCase):

    def _assert_creates_global_root(self, model_class):
        call_command('create_global_roots', verbosity=0)
        qs = model_class.objects.filter(name='!ROOT!')
        self.assertEquals(qs.count(), 1)
        self.assertIsNone(qs[0].parent)

    def _assert_changes_existing_roots(self, model_class):
        if model_class == Source:
            model_factory = SourceFactory
        elif model_class == Category:
            model_factory = CategoryFactory
        elif model_class == Format:
            model_factory = FormatFactory
        else:
            raise Exception('Do not know the factory of the %s model' % model_class)

        # create some root instances
        instance1 = model_factory(parent=None)
        instance2 = model_factory(parent=None)
        instance3 = model_factory(parent=None)

        assert model_class.objects.filter(parent__isnull=True).count(), 3
        call_command('create_global_roots', verbosity=0)

        # now testing
        qs = model_class.objects.filter(parent__isnull=True)
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].name, '!ROOT!')

        # all old roots moved to global root children
        self.assertIsNotNone(model_class.objects.get(id=instance1.id).parent)
        self.assertEquals(
            model_class.objects.get(id=instance1.id).parent.name,
            '!ROOT!')

        self.assertIsNotNone(model_class.objects.get(id=instance2.id).parent)
        self.assertEquals(
            model_class.objects.get(id=instance2.id).parent.name,
            '!ROOT!')

        self.assertIsNotNone(model_class.objects.get(id=instance3.id).parent)
        self.assertEquals(
            model_class.objects.get(id=instance3.id).parent.name,
            '!ROOT!')

    def test_creates_source_global_root(self):
        self._assert_creates_global_root(Source)

    def test_creates_format_global_root(self):
        self._assert_creates_global_root(Format)

    def test_creates_category_global_root(self):
        self._assert_creates_global_root(Category)

    def test_changes_existing_source_roots(self):
        self._assert_changes_existing_roots(Source)

    def test_changes_existing_category_roots(self):
        self._assert_changes_existing_roots(Category)

    def test_changes_existing_format_roots(self):
        self._assert_changes_existing_roots(Format)

    def test_does_not_create_source_global_root_twice(self):
        call_command('create_global_roots', verbosity=0)
        qs = Source.objects.filter(name='!ROOT!')
        self.assertEquals(qs.count(), 1)
        self.assertIsNone(qs[0].parent)

        call_command('create_global_roots', verbosity=0)
        qs = Source.objects.filter(name='!ROOT!')
        self.assertEquals(qs.count(), 1)
        self.assertIsNone(qs[0].parent)
