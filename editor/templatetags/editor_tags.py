# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.inclusion_tag('editor/includes/formset_forms.html')
def formset_form(formset, form):
    """ Renders one formset form. """
    return {
        'formset': formset,
        'forms': [form]
    }


@register.inclusion_tag('editor/includes/formset_forms.html')
def formset_forms(formset, forms):
    """ Renders all given forms. """
    return {
        'formset': formset,
        'forms': forms
    }


@register.inclusion_tag('editor/includes/files_block.html')
def files_block(formset, title, block_id):
    """ Renders all given forms. """
    return {
        'title': title,
        'id': block_id,
        'formset': formset
    }
