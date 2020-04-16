from django.contrib import admin

from .models import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ['profiles_mentioned', 'created_by']
    # list_display = (,)
    # list_filter = (,)
    pass
