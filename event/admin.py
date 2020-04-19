from django.contrib import admin

from event.models import Event, Result


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    autocomplete_fields = ['created_by', 'last_modified_by']
    search_fields = ['name', ]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    autocomplete_fields = ['created_by', 'last_modified_by', 'coxswain', 'rowers', 'shell', 'event']
