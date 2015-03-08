# -*- coding: utf-8 -*-

from django.forms import ModelForm

from editor.models import Category


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'parent']
