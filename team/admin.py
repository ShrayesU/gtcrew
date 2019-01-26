from django.contrib import admin
import csv
from django.urls import path
from django.shortcuts import render, redirect
from .forms import CsvImportForm, ProfileForm
#from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Profile, Membership, Squad, Title, Award, AwardGiven, Post, Page

#User = get_user_model()

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('profile', 'squad', 'year', 'semester')
    list_filter = ('squad', 'year','semester',)

class ProfileInline(admin.TabularInline):
    model = Membership
    classes = ['collapse']
    fields = ('semester', 'year', 'profile',)
    ordering = ['-year', 'semester',]
    extra = 0

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'held_by', 'sequence')
    list_filter = ('held_by',)
    list_editable = ('sequence',)
    ordering = ['-held_by', 'sequence',]
    inlines = [ProfileInline,]

@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    inlines = [ProfileInline,]

class AwardGivenInline(admin.TabularInline):
    model = AwardGiven
    classes = ['collapse']
    extra = 0

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    inlines = [AwardGivenInline,]
    
#    def has_add_permission(self, request):
#        return False

class MembershipInline(admin.TabularInline):
    model = Membership
    classes = ['collapse']
    ordering = ['year', '-semester',]
    extra = 0

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['first_name', 'last_name', 'email', 'bio', 'photo', ]}),
        ('Personal',         {'fields': ['gtid', 'birthday', 'major', 'hometown'], 'classes': ['collapse']}),
        ('Date information', {'fields': ['date_created', 'date_updated'], 'classes': ['collapse']}),
    ]
    inlines = [AwardGivenInline, MembershipInline,]
    list_display = ('full_name', 'latest_year_active', 'date_updated')
    readonly_fields = ('full_name', 'date_created', 'date_updated')
    search_fields = ['first_name', 'last_name', 'gtid']
    
    change_list_template = "team/profile_changelist.html"

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
                messages.error(request,'File is not CSV type')
            else:
                reader = csv.DictReader(csv_file.read().decode("utf-8").splitlines())
                for row in reader:
                    row['email'] = row['email'].lower()
                    row['first_name'] = row['first_name'].title()
                    row['last_name'] = row['last_name'].title()
                    row['hometown'] = row['hometown'].title()
                    row['major'] = row['major'].title()
                    row['title'] = row['title'].title()
                    row['held_by'] = row['held_by'].lower()
                    row['squad'] = row['squad'].title()
                    row['semester'] = row['semester'].upper()
                    p, p_created = Profile.objects.get_or_create(
                        email=row['email'],
                        )
                    pf = ProfileForm(row, instance=p)
                    if pf.is_valid():
                        pf.save()
                    if len(row['title'])>0:
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
                self.message_user(request, "Your csv file has been imported")
                return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

class PostInline(admin.StackedInline):
    model = Post
    fieldsets = [
        (None,               {'fields': ['header1', 'header2', 'photo', 'text',]}),
        ('Optional Link',    {'fields': ['additional_link', 'additional_link_text'], 'classes': ['collapse']}),
        ('Date information', {'fields': ['date_created', 'date_updated'], 'classes': ['collapse']}),
    ]
    classes = ['collapse']
    readonly_fields = ('date_created', 'date_updated')
    extra = 0

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['page', 'template', 'sequence',]}),
        ('Optional Textbox', {'fields': ['header1', 'header2', 'text',], 'classes': ['collapse']}),
    ]
    inlines = [PostInline,]
    list_display = ('page', 'sequence',)
    list_editable = ('sequence',)
    ordering = ['sequence',]
