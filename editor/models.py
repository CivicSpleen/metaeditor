# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Source(MPTTModel):
    name = models.CharField(
        max_length=200,
        help_text='Formal name of the source. such as "Department of Health and Human Services".')
    abbreviation = models.CharField(
        max_length=50,
        help_text='A common abbreviation for the name of the source, such as "HHS".')
    domain = models.CharField(
        max_length=50,
        help_text='A short string, by default derived from the Home page url.')
    homepage = models.URLField(
        help_text='URL of the home page for the organization.')
    about = models.TextField(
        help_text='Freeform text, paragraph length.')
    parent = TreeForeignKey(
        'self', null=True, blank=True,
        help_text='A link to another source.')
    categories = models.ManyToManyField(
        'Category',
        help_text='Multiple links to names of categories.')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('source-update', kwargs={'pk': self.id})

    @staticmethod
    def get_create_url():
        return reverse('source-create')


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
        return reverse('category-update', kwargs={'pk': self.id})

    @staticmethod
    def get_create_url():
        return reverse('category-create')


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
        return reverse('format-update', kwargs={'pk': self.id})

    @staticmethod
    def get_create_url():
        return reverse('format-create')


class Dataset(models.Model):
    NATIONAL = 'national'
    STATE = 'state'
    COUNTY = 'county'
    SUB_COUNTY = 'sub-county'

    COVERAGE_CHOICES = (
        (NATIONAL, 'National'),
        (STATE, 'State'),
        (COUNTY, 'County'),
        (SUB_COUNTY, 'Sub county'))

    STATE_AND_COUNTY = 'state_and_county'

    REGION_CHOICES = (
        (STATE, 'State'),
        (STATE_AND_COUNTY, 'State and county'))

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
        help_text='Distinguished this dataset from similar datasets.')
    start_year = models.IntegerField(
        help_text='The first year for which the dataset has data.')
    end_year = models.IntegerField(
        help_text='The last year for which the dataset has data.')
    coverage = models.CharField(
        max_length=50,
        choices=COVERAGE_CHOICES)
    region = models.CharField(
        max_length=100,
        choices=REGION_CHOICES)
    page = models.URLField(
        help_text='URL of a web page about the dataset.')
    download_page = models.URLField(
        help_text='URL of a web page where dataset files can be downloaded.')
    contacts = models.TextField(
        help_text='Freeform text of people to email or call about the dataset. ')
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

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('dataset-update', kwargs={'pk': self.id})


class File(models.Model):
    dataset = models.ForeignKey(Dataset)
    file_format = models.ForeignKey(Format)
    f = models.FileField(upload_to='uploads')

    class Meta:
        abstract = True


class DataFile(File):
    pass


class DocumentFile(File):
    pass
