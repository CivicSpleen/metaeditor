# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def give_perm(user, model_class, codename):
    """ Gives user permission to perform `codename` action on `model_class` model. """
    # give permission to create category
    content_type = ContentType.objects.get_for_model(model_class)
    permission = Permission.objects.get(content_type=content_type, codename=codename)
    user.user_permissions.add(permission)
