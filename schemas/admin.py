from django.contrib import admin

from .models import Schema, Dataset


class DatasetInline(admin.TabularInline):
    model = Dataset
    extra = 0


class SchemaAdmin(admin.ModelAdmin):
    inlines = [
        DatasetInline,
    ]


admin.site.register(Schema, SchemaAdmin)
admin.site.register(Dataset)
