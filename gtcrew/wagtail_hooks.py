from django.urls import reverse, re_path
from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.views.snippets import SnippetViewSetGroup

from award.models import Recipient
from event.models import Result
from gtcrew.views import PeopleReportView
from team.models import Title, Squad, Profile


# class ProfileModelAdmin(ModelAdmin):
#     model = Profile
#     menu_icon = 'user'
#     menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
#     list_display = ('first_name', 'last_name', 'status')
#     list_filter = ('status',)
#     search_fields = ('first_name', 'last_name', 'gtid')


# class MembershipModelAdmin(ModelAdmin):
#     model = Membership
#     menu_icon = 'users'
#     menu_order = 300
#     list_display = ('year', 'semester', 'profile',)  # 'profile__first_name', 'profile__last_name')
#     list_filter = ('title', 'public',)
#     search_fields = ('profile__first_name', 'profile__last_name', 'profile__gtid')


class RecipientViewSet(SnippetViewSet):
    model = Recipient
    list_display = ('year', 'page', 'person_page',)
    list_filter = ('page', 'year')


class TitleViewSet(SnippetViewSet):
    model = Title
    list_display = ('title', 'held_by',)
    search_fields = ('title',)
    list_filter = ('held_by',)


class SquadViewSet(SnippetViewSet):
    model = Squad
    search_fields = ('squad',)


class ResultViewSet(SnippetViewSet):
    model = Result
    list_per_page = 10
    list_display = ('page', 'entry', 'distance', 'total_time_string', 'pace_string', 'watts', 'pace', 'racer_count')
    search_fields = ('entry', 'page__title')
    list_filter = ('date', 'squad', 'page__regatta', 'distance', 'lightweight')
    inspect_view_enabled = True


class TeamDetailViewSet(SnippetViewSetGroup):
    menu_label = 'Team Details'
    menu_icon = 'group'
    menu_order = 200
    items = (SquadViewSet, TitleViewSet, RecipientViewSet, ResultViewSet)


# register_snippet(ProfileModelAdmin)
# register_snippet(MembershipModelAdmin)
register_snippet(TeamDetailViewSet)


@hooks.register('register_reports_menu_item')
def register_people_report_menu_item():
    return AdminOnlyMenuItem("Term Pages with people list", reverse('people_report'),
                             classname='icon icon-' + PeopleReportView.header_icon, order=700)


@hooks.register('register_admin_urls')
def register_people_report_url():
    return [
        re_path(r'^reports/people/$', PeopleReportView.as_view(), name='people_report'),
    ]


@hooks.register('construct_main_menu')
def hide_analytics_menu_item(request, menu_items):
    # TODO: Remove this after fixing the analytics dashboard in wagalytics
    menu_items[:] = [item for item in menu_items if item.name != 'analytics']
