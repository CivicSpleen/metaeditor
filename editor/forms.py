# -*- coding: utf-8 -*-
from logging import getLogger

from django import forms
from django.forms.models import inlineformset_factory

from editor.models import Dataset, DataFile, DocumentFile, Category,\
    Format, Source

logger = getLogger(__name__)


class NodeBaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NodeBaseForm, self).__init__(*args, **kwargs)

        # display some fields horizontally
        for field_name in getattr(self, 'horizontal_fields', []):
            self.fields[field_name].horizontal = True

        # do not render root node
        self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(parent__isnull=True)

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if not parent:
            # find and return root
            try:
                parent = self.Meta.model.objects.get(parent__isnull=True)
            except self.Meta.model.DoesNotExist:
                logger.warning('%s model does not have root node. Create it.' % self.Meta.model)
        return parent


class DatasetForm(forms.ModelForm):

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(parent__isnull=False).order_by('name'),
        widget=forms.CheckboxSelectMultiple(),
        required=False)

    formats = forms.ModelMultipleChoiceField(
        queryset=Format.objects.filter(parent__isnull=False).order_by('name'),
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
            # may be empty if it is an update action
            instance.source = self.source
        instance.user = self.user
        instance.save()
        self.save_m2m()
        return instance


class ScrapeForm(forms.Form):
    url = forms.URLField(required=True)


class SourceForm(NodeBaseForm):

    horizontal_fields = ['name', 'parent', 'abbreviation', 'domain', 'homepage']

    class Meta:
        model = Source
        fields = ['name', 'parent', 'abbreviation', 'domain', 'homepage', 'about', 'categories']

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        self.fields['about'].widget.attrs['rows'] = 4

        # do not render root of the category
        self.fields['categories'].queryset = self.fields['categories'].queryset.exclude(parent__isnull=True)


class CategoryForm(NodeBaseForm):

    horizontal_fields = ['name', 'parent']

    class Meta:
        model = Category
        fields = ['name', 'parent']


class FormatForm(NodeBaseForm):

    horizontal_fields = ['name', 'parent']

    class Meta:
        model = Format
        fields = ['name', 'parent']


class FileBaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FileBaseForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'name'
        self.fields['url'].widget.attrs['class'] = 'url'


class DataFileForm(FileBaseForm):

    class Meta:
        model = DataFile
        fields = ['name', 'dataset', 'file_format', 'url']


class DocumentFileForm(FileBaseForm):

    class Meta:
        model = DocumentFile
        fields = ['name', 'dataset', 'file_format', 'url']

DataFileFormset = inlineformset_factory(
    Dataset, DataFile, form=DataFileForm, extra=1)
DocumentFileFormset = inlineformset_factory(
    Dataset, DocumentFile, form=DocumentFileForm, extra=1)
