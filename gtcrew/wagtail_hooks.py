from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from team.models import Profile, Award, Title, Squad


class AwardModelAdmin(ModelAdmin):
    model = Award
    search_fields = ('award',)


class TitleModelAdmin(ModelAdmin):
    model = Title
    search_fields = ('title',)


class SquadModelAdmin(ModelAdmin):
    model = Squad
    search_fields = ('squad',)


class TeamDetailAdminGroup(ModelAdminGroup):
    menu_label = 'Team Details'
    menu_icon = 'fa-suitcase'
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (AwardModelAdmin, TitleModelAdmin, SquadModelAdmin)


class ProfileModelAdmin(ModelAdmin):
    model = Profile
    menu_icon = 'user'
    menu_order = 300
    list_display = ('first_name', 'last_name', 'status')
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'gtid')


modeladmin_register(TeamDetailAdminGroup)
modeladmin_register(ProfileModelAdmin)
