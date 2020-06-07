from django.contrib import admin
from django_summernote.admin import SummernoteModelAdminMixin

from campaign.models import Donation, Campaign


class DonationInline(admin.TabularInline):
    model = Donation
    fields = ('donation_amount', 'donor')
    autocomplete_fields = ['donor', ]
    extra = 0


@admin.register(Campaign)
class CampaignAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    summernote_fields = '__all__'
    list_display = ('title', 'goal', 'donation_total', 'date_added', 'date_updated')
    list_filter = ('date_added', 'end_date', )
    search_fields = ['title', ]
    readonly_fields = ('date_added', 'date_updated', 'slug')
    autocomplete_fields = ['created_by', 'last_modified_by']
    inlines = [DonationInline, ]


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'donation_amount', 'campaign', 'date_added', )
    list_filter = ('campaign', )
    readonly_fields = ('date_added', 'date_updated', )
    autocomplete_fields = ['donor', 'created_by', 'last_modified_by', 'campaign']
