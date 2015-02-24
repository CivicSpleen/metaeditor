from django.forms import ModelForm, Form

from editor.models import Category


class CategoryForm(ModelForm):
    class Meta:
        model = Category