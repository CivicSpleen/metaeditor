# -*- coding: utf-8 -*-
import os
import shutil

from django import forms
from django.conf import settings
from django.forms.models import inlineformset_factory

from editor.models import Dataset, DataFile, DocumentFile, get_upload_path


class DatasetForm(forms.ModelForm):

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
        return instance


class FileBaseForm(forms.ModelForm):
    upload_id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(FileBaseForm, self).__init__(*args, **kwargs)
        self.fields['f'].required = False

        # it is time to submit the format of the file.
        self.fields['file_format'].required = True
        self.fields['upload_id'].widget.attrs = {'class': 'upload_id'}

    def save(self, *args, **kwargs):
        if 'upload_id' in self.cleaned_data:
            # id of the preloaded file given. Extend it with format and dataset
            instance = self._meta.model.objects.get(id=self.cleaned_data['upload_id'])

            instance.dataset = self.cleaned_data['dataset']
            instance.file_format = self.cleaned_data['file_format']

            # move uploaded file to the dataset folder.
            upload_to = get_upload_path(instance, '')
            full_path = os.path.join(settings.MEDIA_ROOT, upload_to)
            if not os.path.exists(full_path):
                os.makedirs(full_path)

            new_path = os.path.join(full_path, os.path.basename(instance.f.name))

            shutil.move(instance.f.path, new_path)
            instance.f = get_upload_path(instance, os.path.basename(instance.f.name))
            instance.save()
            return instance
        else:
            return super(FileBaseForm, self).save(*args, **kwargs)


class DataFileForm(FileBaseForm):

    class Meta:
        model = DataFile
        fields = ['f', 'file_format']


class DocumentFileForm(FileBaseForm):

    class Meta:
        model = DocumentFile
        fields = ['f', 'file_format']

DataFileFormset = inlineformset_factory(
    Dataset, DataFile, form=DataFileForm, extra=0)
DocumentFileFormset = inlineformset_factory(
    Dataset, DocumentFile, form=DocumentFileForm, extra=0)
