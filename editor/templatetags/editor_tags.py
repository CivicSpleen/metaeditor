# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.inclusion_tag('editor/includes/formset_forms.html')
def formset_form(form):
    """ Renders one formset form. """
    return {
        'forms': [form]
    }


@register.inclusion_tag('editor/includes/formset_forms.html')
def formset_forms(forms):
    """ Renders all given forms. """
    return {
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
