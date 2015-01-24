from django.contrib import admin
from editor.models import Source, Category, Format, Dataset, DataFile, DocumentFile

admin.site.register(Source)
admin.site.register(Category)
admin.site.register(Format)
admin.site.register(Dataset)
admin.site.register(DataFile)
admin.site.register(DocumentFile)

