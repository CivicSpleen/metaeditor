# -*- coding: utf-8 -*-

from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from editor.models import Source, Category, Format, Dataset, DataFile, DocumentFile


class MPTTCategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


class MPTTFormatAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


class MPTTSourceAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


class DataFileInline(admin.TabularInline):
    model = DataFile
    extra = 1


class DocumentFileInline(admin.TabularInline):
    model = DocumentFile
    extra = 1


class DatasetAdmin(admin.ModelAdmin):
    model = Dataset
    inlines = [
        DataFileInline,
        DocumentFileInline]

admin.site.register(Source, MPTTSourceAdmin)
admin.site.register(Category, MPTTCategoryAdmin)
admin.site.register(Format, MPTTFormatAdmin)

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(DataFile)
admin.site.register(DocumentFile)
