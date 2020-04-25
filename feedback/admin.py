from django.contrib import admin

from .models import Feedback
from .utils import CLOSED


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'date_added', 'status')
    list_filter = ('date_added',)
    actions = ['set_status_to_closed']

    def set_status_to_closed(self, request, queryset):
        rows_updated = queryset.update(status=CLOSED)
        if rows_updated == 1:
            message_bit = "1 case was"
        else:
            message_bit = "%s cases were" % rows_updated
        self.message_user(request, "%s successfully set to Closed." % message_bit)
