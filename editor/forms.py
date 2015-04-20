# -*- coding: utf-8 -*-
from logging import getLogger

from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.html import format_html

from editor.models import Dataset, DataFile, DocumentFile, Category,\
    Format, Source, Extension
from editor.utils import truncate_value

logger = getLogger(__name__)


class LinkWidget(forms.URLInput):

    def __init__(self, show_link=False, *args, **kwargs):
        super(LinkWidget, self).__init__(*args, **kwargs)
        self.show_link = show_link

    def render(self, name, value, attrs=None):
        if self.show_link:
            link_style = ''
            if not attrs:
                attrs = {'type': 'hidden'}
            else:
                attrs['type'] = 'hidden'
        else:
            link_style = 'style=display:none;'

        input_html = super(LinkWidget, self).render(name, value, attrs)
        if value is None:
            value = '#'

        truncated_value = truncate_value(value)

        a_html = format_html(
            '<a class="link" href="{0}" title="{1}" {2}>{1}</a>',
            value,
            truncated_value,
            link_style)
        return format_html('{0}\n{1}', input_html, a_html)


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
        if self.instance and self.instance.id and self.instance.datafile_set.exists():
            self.fields['formats'].widget.attrs['disabled'] = 'disabled'

        # change start and end years labels
        self.fields['start_year'].label = 'from'
        self.fields['end_year'].label = 'to'

        # move help text to the title for start and end year
        self.fields['start_year'].widget.attrs['title'] = self.fields['start_year'].help_text
        self.fields['start_year'].help_text = ''

        self.fields['end_year'].widget.attrs['title'] = self.fields['end_year'].help_text
        self.fields['end_year'].help_text = ''

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
    extensions = forms.CharField(
        required=False,
        help_text='Comma separated list of the extensions.')

    horizontal_fields = ['name', 'parent']

    class Meta:
        model = Format
        fields = ['name', 'parent']

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            self.fields['extensions'].initial = ', '.join([x.name for x in self.instance.extension_set.all()])

    def clean_extensions(self):
        extensions = self.cleaned_data.get('extensions', '')
        if '.' in extensions:
            raise forms.ValidationError('Extensions should not contain dots.')

        if '*' in extensions:
            raise forms.ValidationError('Extensions should not contains asterisks.')
        return extensions

    def save(self, *args, **kwargs):
        format_instance = super(self.__class__, self).save(*args, **kwargs)
        extensions = self.cleaned_data.get('extensions')
        Extension.update(format_instance, extensions)
        return format_instance


class FileBaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FileBaseForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            show_link = True
        else:
            show_link = False
        self.fields['url'].widget = LinkWidget(show_link=show_link)
        self.fields['name'].widget.attrs['class'] = 'name'
        self.fields['url'].widget.attrs['class'] = 'url'

        # remove labels from all of the fields
        self.fields['name'].label = ''
        self.fields['file_format'].label = ''
        self.fields['url'].label = ''

        # add title for all of the fields
        self.fields['name'].widget.attrs['title'] = 'Name of the file.'
        self.fields['file_format'].widget.attrs['title'] = 'Format of the file.'
        self.fields['url'].widget.attrs['title'] = 'URL of the file.'

        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['url'].widget.attrs['placeholder'] = 'URL'

        # do not show root format
        self.fields['file_format'].queryset = self.fields['file_format'].queryset.exclude(parent__isnull=True)


class DataFileForm(FileBaseForm):

    class Meta:
        model = DataFile
        fields = ['name', 'dataset', 'file_format', 'url']


class DocumentFileForm(FileBaseForm):

    class Meta:
        model = DocumentFile
        fields = ['name', 'dataset', 'file_format', 'url']


class MyFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(MyFormSet, self).add_fields(form, index)
        form.fields['DELETE'].label = 'Del'

DataFileFormset = inlineformset_factory(
    Dataset, DataFile, form=DataFileForm, formset=MyFormSet, extra=1)
DocumentFileFormset = inlineformset_factory(
    Dataset, DocumentFile, form=DocumentFileForm, formset=MyFormSet, extra=1)
