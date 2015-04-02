# -*- coding: utf-8 -*-
import os
import csv

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from editor.models import Source
from editor.tests.factories import SourceFactory


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
