import csv

from django.contrib import admin
# from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import path
from django_summernote.admin import SummernoteModelAdminMixin

from .forms import CsvImportForm, ProfileForm
from .models import Profile, EmailAddress, Membership, Squad, Title, Award, AwardGiven, Post, Page

# User = get_user_model()

admin.site.register(Squad)


@admin.register(EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    search_fields = ['email', 'profile__first_name', 'profile__last_name']


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    search_fields = ['profile__first_name', 'profile__last_name']
    list_filter = ('public',)
    autocomplete_fields = ['profile']
    actions = ['make_public', ]

    def make_public(self, request, queryset):
        rows_updated = queryset.update(public=True)
        if rows_updated == 1:
            message_bit = "1 membership was"
        else:
            message_bit = "%s memberships were" % rows_updated
        self.message_user(request, "%s successfully marked as public." % message_bit)


class AwardGivenInline(admin.TabularInline):
    model = AwardGiven
    classes = ['collapse']
    autocomplete_fields = ['profile']
    extra = 0


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    inlines = [AwardGivenInline, ]


class MembershipInline(admin.TabularInline):
    model = Membership
    classes = ['collapse']
    ordering = ['year', '-semester', ]
    autocomplete_fields = ['profile']
    extra = 0


class MembershipInlineTitle(MembershipInline):
    ordering = ['-year', 'semester', ]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'held_by', 'sequence')
    list_filter = ('held_by',)
    list_editable = ('sequence',)
    ordering = ['-held_by', 'sequence', ]
    inlines = [MembershipInline, ]


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 0


@admin.register(Profile)
class ProfileAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    summernote_fields = '__all__'
    fieldsets = [
        (None, {'fields': ['first_name', 'last_name', 'gtid', 'status', 'public', 'owner', 'bio', 'photo', ]}),
        ('Personal', {'fields': ['birthday', 'major', 'hometown'], 'classes': ['collapse']}),
        ('Date information', {'fields': ['date_created', 'date_updated'], 'classes': ['collapse']}),
    ]
    inlines = [EmailAddressInline, AwardGivenInline, MembershipInline, ]
    list_display = ('first_name', 'last_name', 'gtid', 'latest_year_active', 'date_updated')
    list_filter = ('status', 'public', 'membership__squad', 'membership__year', 'membership__semester')
    readonly_fields = ('date_created', 'date_updated')
    search_fields = ['first_name', 'last_name', 'gtid']
    autocomplete_fields = ['owner']
    actions = ['make_public', ]
    change_list_template = "team/profile_changelist.html"

    def make_public(self, request, queryset):
        rows_updated = queryset.update(public=True)
        if rows_updated == 1:
            message_bit = "1 profile was"
        else:
            message_bit = "%s profiles were" % rows_updated
        self.message_user(request, "%s successfully marked as public." % message_bit)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
            else:
                reader = csv.DictReader(csv_file.read().decode("utf-8").splitlines())
                for row in reader:
                    try:
                        row['email'] = row['email'].lower()  # required
                    except KeyError:
                        pass
                    try:
                        row['first_name'] = row['first_name'].title()  # required
                    except KeyError:
                        pass
                    try:
                        row['last_name'] = row['last_name'].title()  # required
                    except KeyError:
                        pass
                    try:
                        row['hometown'] = row['hometown'].title()
                    except KeyError:
                        pass
                    try:
                        row['major'] = row['major'].title()
                    except KeyError:
                        pass
                    try:
                        row['title'] = row['title'].title()
                    except KeyError:
                        pass
                    try:
                        row['held_by'] = row['held_by'].lower()
                    except KeyError:
                        pass
                    try:
                        row['squad'] = row['squad'].title()
                    except KeyError:
                        pass
                    try:
                        row['semester'] = row['semester'].upper()  # required
                    except KeyError:
                        pass
                    try:
                        row['year'] = row['year']  # required
                    except KeyError:
                        pass
                    p, p_created = Profile.objects.get_or_create(
                        gtid=row['gtid'],
                    )
                    pf = ProfileForm(row, instance=p)
                    if pf.is_valid():
                        pf.save()
                    if len(row['title']) > 0:
                        m, m_created = Membership.objects.update_or_create(
                            profile=p,
                            semester=row['semester'],
                            year=row['year'],
                            squad=Squad.objects.get(squad=row['squad']),
                            title=Title.objects.get(
                                title=row['title'],
                                held_by=row['held_by'],
                            )
                        )
                    else:
                        m, m_created = Membership.objects.update_or_create(
                            profile=p,
                            semester=row['semester'],
                            year=row['year'],
                            squad=Squad.objects.get(squad=row['squad']),
                        )
                    e, e_saved = EmailAddress.objects.get_or_create(
                        email=row['email'],
                        profile=p,
                    )
                self.message_user(request, "Your csv file has been imported")
                return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )


class PostInline(SummernoteModelAdminMixin, admin.StackedInline):
    model = Post
    summernote_fields = '__all__'
    fieldsets = [
        (None, {'fields': ['header1', 'header2', 'photo', 'text', 'public', ]}),
        ('Optional Link', {'fields': ['additional_link', 'additional_link_text'], 'classes': ['collapse']}),
        ('Optional Attachment', {'fields': ['document', 'document_name'], 'classes': ['collapse']}),
        ('Date information', {'fields': ['date_created', 'date_updated'], 'classes': ['collapse']}),
    ]
    classes = ['collapse']
    readonly_fields = ('date_created', 'date_updated')
    extra = 0


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['page', 'template', 'sequence', 'public', ]}),
    ]
    inlines = [PostInline, ]
    list_display = ('page', 'public', 'sequence',)
    list_editable = ('public', 'sequence',)
    ordering = ['sequence', ]
