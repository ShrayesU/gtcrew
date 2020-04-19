from django.contrib import admin

from .models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    autocomplete_fields = ['created_by', 'last_modified_by']
    search_fields = ['name', ]
    # list_display = (,)
    # list_filter = (,)
    pass
