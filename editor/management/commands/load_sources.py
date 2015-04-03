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

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.id_map = {}

    def _create_node(self, node, verbosity=1):
        """ Creates node and returns it. """
        if verbosity > 0:
            self.stdout.write('Starting to create %s node' % node['unique_name'])

        # find parent node.
        if node['parent_id']:
            parent = self.id_map[node['parent_id']].get('instance')
            if not parent:
                # parent instance was not created yet
                parent = self._create_node(
                    self.id_map[node['parent_id']], verbosity=verbosity)
        else:
            # root node found
            parent = None

        # get or create current node.
        try:
            node_instance = Source.objects.get(name=node['unique_name'])
        except Source.DoesNotExist:
            node_instance = Source.objects.create(
                name=node['unique_name'],
                parent=parent,
                abbreviation=node['abbreviation'],
                domain=node['domain'],
                homepage=node['homepage'],
                about=node['about'])
            self.id_map[node['id']]['instance'] = node_instance

        # some validation
        assert node_instance.name == node['unique_name']
        if node_instance.parent:
            assert node_instance.parent.name == self.id_map[node['parent_id']]['unique_name']

        if verbosity > 0:
            self.stdout.write('Node %s created' % node['unique_name'])
        return node_instance

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        if verbosity > 0:
            self.stdout.write('Starting to load sources...')

        sources = os.path.join(
            settings.BASE_DIR, '../', 'editor', 'data', 'sources.csv')

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

        with open(sources) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # add unique name to properly process repeated names
                row['unique_name'] = '%s|%s' % (row['name'], row['id'])
                self.id_map[row['id']] = row

        for node in self.id_map.values():
            if Source.objects.filter(name=node['unique_name']).exists():
                if verbosity > 0:
                    self.stdout.write(
                        'Node %s already exists. Do nothing.' % node['unique_name'])
                continue
            self._create_node(node, verbosity=verbosity)

        Source.objects.rebuild()

        if verbosity > 0:
            self.stdout.write('Removing csv id from name...')
        for source in Source.objects.all():
            source.name = source.name.split('|')[0]
            source.save()

        if verbosity > 0:
            self.stdout.write('Done.')
