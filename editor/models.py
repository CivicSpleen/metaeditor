# -*- coding: utf-8 -*-
import os
from logging import getLogger

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from editor.constants import REGION_CHOICES

from compat import ambry_utils

logger = getLogger(__name__)


class Source(MPTTModel):
    name = models.CharField(
        max_length=200,
        help_text='Formal name of the source. such as "Department of Health and Human Services".')
    abbreviation = models.CharField(
        max_length=50,
        null=True, blank=True,
        help_text='A common abbreviation for the name of the source, such as "HHS".')
    domain = models.CharField(
        max_length=50,
        null=True, blank=True,
        help_text='A short string, by default derived from the Home page url.')
    homepage = models.URLField(
        help_text='URL of the home page for the organization.')
    about = models.TextField(
        help_text='Freeform text, paragraph length.',
        null=True, blank=True)
    parent = TreeForeignKey(
        'self', null=True, blank=True,
        help_text='A link to another source.')
    categories = models.ManyToManyField(
        'Category',
        null=True, blank=True,
        help_text='Multiple links to names of categories.')
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='created_sources',
        help_text='User who created that source.')
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='updated_sources',
        help_text='User who last edited that source.')

    def __unicode__(self):
        if self.abbreviation:
            return u'%s (%s)' % (self.name, self.abbreviation)
        return self.name

    def get_absolute_url(self):
        return reverse('editor:source-update', kwargs={'pk': self.id})

    def get_dataset_create_url(self):
        return reverse('editor:dataset-create', kwargs={'source_pk': self.id})

    @staticmethod
    def get_create_url():
        return reverse('editor:source-create')


class Category(MPTTModel):
    name = models.CharField(
        max_length=100,
        help_text='The name of the category')
    parent = TreeForeignKey(
        'self', null=True, blank=True,
        help_text='A link to another category')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_absolute_url(self):
        return reverse('editor:category-update', kwargs={'pk': self.id})

    @staticmethod
    def get_create_url():
        return reverse('editor:category-create')


class Format(MPTTModel):
    name = models.CharField(
        max_length=100,
        help_text='The name of the format.')
    parent = TreeForeignKey(
        'self', null=True, blank=True,
        help_text='A link to another format.')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('editor:format-update', kwargs={'pk': self.id})

    @staticmethod
    def get_create_url():
        return reverse('editor:format-create')

    @classmethod
    def guess_by_path(cls, path):

        # get extension from path
        name, ext = os.path.splitext(path)

        # find first match
        extensions = Extension.objects.filter(name=ext.strip('.')).order_by('-id')[:1]
        if extensions:
            return extensions[0].format
        logger.warning('Format for %s extension was not found.' % ext)
        return None


class Extension(models.Model):
    name = models.CharField(
        max_length=20,
        help_text='The name of the extension.',
        db_index=True)
    format = models.ForeignKey(Format)

    class Meta:
        unique_together = (('name', 'format'),)

    @classmethod
    def update(cls, format, extensions):
        """ Adds new extensions and removes missed.

        Args:
            format (Format):
            extensions (str): comma separated string of the extensions or empty string.
        """

        # convert to list
        extensions = [x.strip() for x in extensions.split(',')]

        # create new
        for extension in extensions:
            if not extension:
                # empty extension within list
                continue
            cls.objects.get_or_create(
                format=format, name=extension)

        # delete all missed
        cls.objects\
            .filter(format=format)\
            .exclude(name__in=extensions)\
            .delete()


class Dataset(models.Model):
    source = models.ForeignKey(
        Source,
        help_text='Source of the dataset.')
    title = models.CharField(
        max_length=200,
        help_text='The title of the dataset.')
    categories = models.ManyToManyField(
        Category,
        help_text='Multiple links to names of categories.')
    variant = models.CharField(
        max_length=100,
        null=True, blank=True,
        help_text='Distinguished this dataset from similar datasets.')
    start_year = models.IntegerField(
        help_text='The first year for which the dataset has data.')
    end_year = models.IntegerField(
        help_text='The last year for which the dataset has data.')
    coverage = models.CharField(
        'Geo Coverage',
        max_length=50)
    region = models.CharField(
        'Geo Grain',
        max_length=100,
        choices=REGION_CHOICES)
    page = models.URLField(
        help_text='URL of a web page about the dataset.')
    download_page = models.URLField(
        null=True, blank=True,
        help_text='URL of a web page where dataset files can be downloaded.')
    contacts = models.TextField(
        null=True, blank=True,
        help_text='Freeform text of people to email or call about the dataset. ')
    about = models.TextField(
        null=True, blank=True,
        help_text='Freeform text about the dataset.')
    formats = models.ManyToManyField(
        Format,
        help_text='Collection of Formats associated with this dataset.')
    is_complex = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    has_restricted_version = models.BooleanField(default=False)
    has_restrictive_licensing = models.BooleanField(default=False)
    has_direct_public_download = models.BooleanField(default=False)
    entry_time_minutes = models.IntegerField(
        help_text='A record of how long the user spent creating the record.')
    user = models.ForeignKey(
        User,
        help_text='Link to the user that edited this dataset. ')
    vid = models.CharField(
        max_length=20, null=True, blank=True, unique=True,
        help_text='An unique number from ambry.')

    def update_formats(self):
        """ Gets all formats from datafiles of the dataset and saves formats with dataset. """
        formats_to_add = [x.file_format for x in self.datafile_set.all()]
        if formats_to_add:
            self.formats.add(*formats_to_add)

            # remove redundant formats
            self.formats.exclude(id__in=[x.id for x in formats_to_add]).delete()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('editor:dataset-update', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        if not self.vid:
            self.vid = ambry_utils.get_vid()
        super(self.__class__, self).save(*args, **kwargs)


class File(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    dataset = models.ForeignKey(Dataset)
    file_format = models.ForeignKey(Format)
    created = models.DateTimeField(
        auto_now_add=True,
        help_text='Creation date and time')
    url = models.URLField(max_length=500)

    class Meta:
        abstract = True


class DataFile(File):

    def save(self, *args, **kwargs):
        super(self.__class__, self).save()
        self.dataset.update_formats()


class DocumentFile(File):
    pass
