from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    homepage = models.URLField()
    about = models.TextField()
    parent = models.ForeignKey('self', null=True)
    categories = models.ManyToManyField("Category")

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True)

class Format(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True)

class Dataset(models.Model):
    title = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    variant = models.CharField(max_length=100)
    start_year = models.
    end_year = 
    coverage_type = models.CharField(max_length=50)
    coverage_name = models.CharField(max_length=100)
    page = models.URLField()
    download_page = models.URLField()
    contact = models.TextField()


class File(models.Model):
    class Meta:
        abstract = True

class DataFile(File):


class DocumentFile(File):


class File(models.Model):
    class Meta:
        abstract = True

class DataFile(File):


class DocumentFile(File):


