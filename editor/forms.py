# -*- coding: utf-8 -*-
from django import forms

from editor.models import Dataset, DataFile, DocumentFile, Format


class DatasetForm(forms.ModelForm):
    data_file = forms.FileField(required=False)
    data_file_format = forms.ModelChoiceField(Format.objects.all(), required=False)
    document_file = forms.FileField(required=False)
    document_file_format = forms.ModelChoiceField(Format.objects.all(), required=False)

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

    def clean(self):
        cd = self.cleaned_data
        if cd.get('data_file') and not cd.get('data_file_format'):
            raise forms.ValidationError(
                'Data file format is required field if you are uploading data file.')
        if cd.get('document_file') and not cd.get('document_file_format'):
            raise forms.ValidationError(
                'Document file format is required field if you are uploading document file.')
        return cd

    def save(self, *args, **kwargs):
        instance = super(DatasetForm, self).save(commit=False, *args, **kwargs)
        if self.source:
            # may be empty if it is update action
            instance.source = self.source
        instance.user = self.user
        instance.save()
        if self.cleaned_data.get('data_file'):
            new_datafile = DataFile(
                f=self.cleaned_data['data_file'],
                file_format=self.cleaned_data['data_file_format'],
                dataset=instance)
            new_datafile.save()

        if self.cleaned_data.get('document_file'):
            new_doc = DocumentFile(
                f=self.cleaned_data['document_file'],
                file_format=self.cleaned_data['document_file_format'],
                dataset=instance)
            new_doc.save()
        return instance
