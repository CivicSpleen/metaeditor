# -*- coding: utf-8 -*-
from subprocess import call

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Sets up ambry search system.'

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        if verbosity > 0:
            self.stdout.write('Starting to set up ambry search system...')

        if verbosity > 0:
            self.stdout.write('Checking ambry version...')

        try:
            import ambry
            version = int(ambry._meta.__version__.strip().replace('.', ''))
            if version < 3705:
                raise CommandError('Metaeditor requires ambry >= 0.3.705')
        except ImportError:
            ambry_docs = 'http://ambry.io/'
            raise CommandError(
                'Ambry is not installed. See {} for instructions.'.format(ambry_docs))

        if verbosity > 0:
            self.stdout.write('Installing ambry config...')

        call(['ambry', 'config', 'install'])

        if verbosity > 0:
            self.stdout.write('Syncing ambry...')

        call(['ambry', 'sync'])

        if verbosity > 0:
            self.stdout.write('Creating search indexes...')

        call(['ambry', 'search', '-R'])

        if verbosity > 0:
            self.stdout.write('Checking search system...')

        l = ambry.library()
        results = [x for x in l.search.search_identifiers('California', limit=1)]
        if not results:
            raise CommandError(
                'Something goes wrong because I couldn\'t find California '
                'term. Try manual setup described in the README.md.')

        if verbosity > 0:
            self.stdout.write('Done.')
