# -*- coding: utf-8 -*-

import factory

from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'test_user%03d' % n)
    first_name = factory.Sequence(lambda n: 'Homer%03d' % n)
    last_name = factory.Sequence(lambda n: 'Simpson%03d' % n)
    email = factory.Sequence(lambda n: 'test_user%03d@localhost' % n)
    password = '1'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)
