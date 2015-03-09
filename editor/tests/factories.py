# -*- coding: utf-8 -*-

import factory
from django.contrib.auth.models import User

from editor.models import Dataset, Format, Category, Source


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'test_user%03d' % n)
    email = factory.Sequence(lambda n: 'test_user%03d@localhost' % n)
    password = '1'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'Test dataset %03d' % n)


class SourceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Source

    name = factory.Sequence(lambda n: 'Test dataset %03d' % n)
    abbreviation = factory.Sequence(lambda n: 'Test dataset %03d abbreviation' % n)
    domain = factory.Sequence(lambda n: 'test.dataset-%03d.org' % n)
    homepage = factory.Sequence(lambda n: 'http://test.dataset-%03d.org' % n)
    about = factory.Sequence(lambda n: 'Test dataset %03d about' % n)

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

    name = factory.Sequence(lambda n: 'Test dataset %03d' % n)


class DatasetFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Dataset

    title = factory.Sequence(lambda n: 'Test dataset %03d' % n)
    source = factory.SubFactory(SourceFactory)
    variant = factory.Sequence(lambda n: 'Test dataset %03d variant' % n)
    start_year = 1976
    end_year = 1976
    coverage = Dataset.COUNTY
    region = Dataset.COUNTY
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
