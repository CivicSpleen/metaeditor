# -*- coding: utf-8 -*-

import factory

from accounts.tests.factories import UserFactory

from editor.constants import REGION_CHOICES
from editor.models import Dataset, Format, Category, Source, Extension, DataFile


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'Test dataset %03d' % n)


class SourceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Source

    name = factory.Sequence(lambda n: 'Test source %03d' % n)
    abbreviation = factory.Sequence(lambda n: 'Test source %03d abbreviation' % n)
    domain = factory.Sequence(lambda n: 'test.source-%03d.org' % n)
    homepage = factory.Sequence(lambda n: 'http://test.source-%03d.org' % n)
    about = factory.Sequence(lambda n: 'Test source %03d about' % n)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of categories were passed in, use them
            for category in extracted:
                self.categories.add(category)


class FormatFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Format

    name = factory.Sequence(lambda n: 'Test format %03d' % n)


class ExtensionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Extension

    name = factory.Sequence(lambda n: 'ext%03d' % n)


class DatasetFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Dataset

    title = factory.Sequence(lambda n: 'Test dataset %03d' % n)
    source = factory.SubFactory(SourceFactory)
    variant = factory.Sequence(lambda n: 'Test dataset %03d variant' % n)
    start_year = 1976
    end_year = 1976
    coverage = ''
    region = REGION_CHOICES[0][0]
    page = factory.Sequence(lambda n: 'Test dataset %03d page' % n)
    download_page = factory.Sequence(lambda n: 'Test dataset %03d download page' % n)
    contacts = factory.Sequence(lambda n: 'Test dataset %03d contacts' % n)
    entry_time_minutes = 11
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of categories were passed in, use them
            for category in extracted:
                self.categories.add(category)

    @factory.post_generation
    def formats(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of formats were passed in, use them
            for format_ in extracted:
                self.categories.add(format_)


class DataFileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = DataFile

    name = factory.Sequence(lambda n: 'Test datafile %03d' % n)
    dataset = factory.SubFactory(DatasetFactory)
    file_format = factory.SubFactory(FormatFactory)
