# -*- coding: utf-8 -*-

from django import template
from django.contrib import messages

register = template.Library()


@register.filter(name='to_bootstrap')
def to_bootstrap(level):
    """ Converts django's message level to bootstrap message level. """
    LEVEL_MAP = {
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger'}
    return LEVEL_MAP[level]
