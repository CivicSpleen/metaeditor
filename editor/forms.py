# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import inlineformset_factory

from editor.models import Dataset, DataFile, DocumentFile, Category,\
    Format


class DatasetForm(forms.ModelForm):

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple(),
        required=False)

    formats = forms.ModelMultipleChoiceField(
        queryset=Format.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple(),
        required=False)

    class Meta:
        model = Dataset
        fields = [
            'title', 'categories', 'variant', 'start_year', 'end_year',
            'coverage', 'region', 'page', 'download_page', 'contacts',
            'formats', 'is_complex', 'is_reviewed', 'has_restricted_version',
            'has_restrictive_licensing', 'has_direct_public_download',
            'entry_time_minutes']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.source = kwargs.pop('source', None)
        super(DatasetForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(DatasetForm, self).save(commit=False, *args, **kwargs)
        if self.source:
            # may be empty if it is update action
            instance.source = self.source
        instance.user = self.user
        instance.save()
        self.save_m2m()
        return instance


class ScrapeForm(forms.Form):
    url = forms.URLField(required=True)


class BaseFileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseFileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'name'
        self.fields['url'].widget.attrs['class'] = 'url'


class DataFileForm(BaseFileForm):

    class Meta:
        model = DataFile
        fields = ['name', 'dataset', 'file_format', 'url']


class DocumentFileForm(BaseFileForm):

    class Meta:
        model = DocumentFile
        fields = ['name', 'dataset', 'file_format', 'url']

DataFileFormset = inlineformset_factory(
    Dataset, DataFile, form=DataFileForm, extra=1)
DocumentFileFormset = inlineformset_factory(
    Dataset, DocumentFile, form=DocumentFileForm, extra=1)
