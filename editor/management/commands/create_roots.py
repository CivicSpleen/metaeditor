# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from editor.models import Source, Format, Category


class Command(BaseCommand):
    help = 'Adds root category for Source, Format and Category models.'

    def _change_root(self, model_class, verbosity=1):
        ROOT_NAME = '!ROOT!'

        try:
            source_root = model_class.objects.get(name=ROOT_NAME)
            if verbosity > 0:
                self.stdout.write(
                    'Root node for %s model already exists. Using it.' % model_class)
        except model_class.DoesNotExist:
            if verbosity > 0:
                self.stdout.write(
                    'Root node for %s model does not exist. Creating...' % model_class)
            source_root = model_class(name=ROOT_NAME)
            source_root.save()

        if verbosity > 0:
            self.stdout.write(
                'Move existing roots to children of the global root.')

        # move existing source roots to children of just created root
        for node in model_class.objects.filter(parent__isnull=True).exclude(id=source_root.id):
            assert node.parent is None
            node.parent = source_root
            node.save()

        model_class.objects.rebuild()

        # validate new root was not changed
        qs = model_class.objects.filter(parent__isnull=True)
        assert qs.count(), 1
        assert qs[0].name == ROOT_NAME

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        if verbosity > 0:
            self.stdout.write('Starting to create global root...')

        self._change_root(Category, verbosity=verbosity)
        self._change_root(Format, verbosity=verbosity)
        self._change_root(Source, verbosity=verbosity)
        if verbosity > 0:
            self.stdout.write('Done.')
