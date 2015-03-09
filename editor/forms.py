# -*- coding: utf-8 -*-

from django.forms import ModelForm

from editor.models import Dataset


class DatasetForm(ModelForm):

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
