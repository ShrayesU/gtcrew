from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from team.models import Profile, Award, Title, Squad, AwardGiven, Membership


class ProfileModelAdmin(ModelAdmin):
    model = Profile
    menu_icon = 'user'
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ('first_name', 'last_name', 'status')
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'gtid')


class MembershipModelAdmin(ModelAdmin):
    model = Membership
    menu_icon = 'users'
    menu_order = 300
    list_display = ('year', 'semester', 'profile', )  # 'profile__first_name', 'profile__last_name')
    list_filter = ('title', 'public', )
    search_fields = ('profile__first_name', 'profile__last_name', 'profile__gtid')


class AwardModelAdmin(ModelAdmin):
    model = Award
    search_fields = ('award',)


class AwardGivenModelAdmin(ModelAdmin):
    model = AwardGiven
    search_fields = ('award__award',)
    list_filter = ('year',)


class TitleModelAdmin(ModelAdmin):
    model = Title
    search_fields = ('title',)
    list_filter = ('held_by',)


class SquadModelAdmin(ModelAdmin):
    model = Squad
    search_fields = ('squad',)


class TeamDetailAdminGroup(ModelAdminGroup):
    menu_label = 'Team Details'
    menu_icon = 'fa-suitcase'
    menu_order = 300
    items = (AwardModelAdmin, AwardGivenModelAdmin, TitleModelAdmin, SquadModelAdmin)


modeladmin_register(ProfileModelAdmin)
modeladmin_register(MembershipModelAdmin)
modeladmin_register(TeamDetailAdminGroup)
