from django.contrib import admin
from editor.models import Source, Category, Format, Dataset, DataFile, DocumentFile
from mptt.admin import MPTTModelAdmin

class MPTTCategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20

class MPTTFormatAdmin(MPTTModelAdmin):
    mptt_level_indent = 20

class MPTTSourceAdmin(MPTTModelAdmin):
    mptt_level_indent = 20

admin.site.register(Source, MPTTSourceAdmin)
admin.site.register(Category, MPTTCategoryAdmin)
admin.site.register(Format, MPTTFormatAdmin)

admin.site.register(Dataset)
admin.site.register(DataFile)
admin.site.register(DocumentFile)

