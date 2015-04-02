# -*- coding: utf-8 -*-
import csv
from optparse import make_option
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from editor.models import Source


class Command(BaseCommand):
    help = 'Loads editor/data/sources.csv to the database.'
    option_list = BaseCommand.option_list + (
        make_option(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete all existing sources'),
        )

    def _create_node(self, node, id_map, verbosity=1):
        """ Creates node and returns it. """
        if verbosity > 0:
            self.stdout.write('Starting to create %s(%s) node' % (node['name'], node['id']))

        # find parent node.
        if node['parent_id']:
            try:
                parent = Source.objects.get(id=node['parent_id'])
            except Source.DoesNotExist:
                parent = self._create_node(
                    id_map[node['parent_id']], id_map, verbosity=verbosity)
        else:
            # root node found
            parent = None

        # create if does not exist.
        try:
            node_instance = Source.objects.get(id=long(node['id']))
        except Source.DoesNotExist:
            node_instance = Source.objects.create(
                id=long(node['id']),
                name=node['name'],
                parent=parent,
                abbreviation=node['abbreviation'],
                domain=node['domain'],
                homepage=node['homepage'],
                about=node['about'])

        # some validation
        assert node_instance.id == long(node['id'])
        if node_instance.parent:
            assert node_instance.parent.id == long(node['parent_id'])

        if verbosity > 0:
            self.stdout.write('Node %s(%s) created' % (node['name'], node['id']))
        return node_instance

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        if verbosity > 0:
            self.stdout.write('Starting to load source...')

        sources = os.path.join(
            settings.BASE_DIR, '../', 'editor', 'data', 'sources.csv')

        id_map = {}
        with open(sources) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id_map[row['id']] = row

        if options['delete']:
            if verbosity > 0:
                self.stdout.write('Deleting all existing sources...')
            Source.objects.all().delete()
            if verbosity > 0:
                self.stdout.write('All existing sources deleted.')
        else:
            if Source.objects.all().exists():
                raise CommandError(
                    'Source model has existing instances. To delete them'
                    ' give --delete option. Warning: this will delete all datasets too.')
        for node in id_map.values():
            if Source.objects.filter(id=node['id'], name=node['name']).exists():
                if verbosity > 0:
                    self.stdout.write(
                        'Node %s(%s) already exists. Do nothing.' % (node['name'], node['id']))
                continue
            self._create_node(node, id_map, verbosity=verbosity)

        Source.objects.rebuild()
        if verbosity > 0:
            self.stdout.write('Done.')
