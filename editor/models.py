from django.db import models
from django.contrib.auth.models import User

class Source(models.Model):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    homepage = models.URLField()
    about = models.TextField()
    parent = models.ForeignKey('self', null=True)
    categories = models.ManyToManyField("Category")
    
    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Format(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True)

    def __unicode__(self):
        return self.name

class Dataset(models.Model):
    title = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    variant = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    coverage_type = models.CharField(max_length=50)
    coverage_name = models.CharField(max_length=100)
    page = models.URLField()
    download_page = models.URLField()
    contacts = models.TextField()
    formats = models.ManyToManyField(Format)
    is_complex = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    has_restricted_version = models.BooleanField(default=False)
    has_restrictive_licensing = models.BooleanField(default=False)
    has_direct_public_download = models.BooleanField(default=False)
    entry_time_minutes = models.IntegerField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

class File(models.Model):
    dataset = models.ForeignKey(Dataset)
    file_format = models.ForeignKey(Format)
    f = models.FileField()
    class Meta:
        abstract = True

class DataFile(File):
    pass

class DocumentFile(File):
    pass

