from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Min
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from event.models import Event, Result
from team.models import Profile
from .forms import EventCreateForm, EventUpdateForm, ResultCreateForm, ResultUpdateForm, ResultPersonalCreateForm


class EventListView(ListView):
    model = Event
    template_name = 'public/event_list.html'


class EventDetailView(DetailView):
    model = Event
    template_name = 'public/view_event.html'


class ResultView(TemplateView):
    model = Result
    template_name = 'public/result.html'


class ResultDataTable(BaseDatatableView):
    model = Result
    columns = ['event.start_datetime', 'event.name', 'name', 'squad.squad', 'time', 'distance']

    def get_initial_queryset(self):
        return Result.objects.filter(event_isnull=False)


# Private Member Views: Event


class EventListViewPrivate(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'private/events.html'
    paginate_by = 10
    ordering = ['-date_added', ]

    def get_context_data(self, **kwargs):
        context = super(EventListViewPrivate, self).get_context_data(**kwargs)

        # custom pagination numbers/pages
        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number
        max_shown = 7  # odd number

        if num_pages <= max_shown or page_no <= (max_shown // 2 + 1):
            pages = [x for x in range(1, min(num_pages + 1, max_shown + 1))]
        elif page_no > num_pages - (max_shown // 2 + 1):
            pages = [x for x in range(num_pages - max_shown + 1, num_pages + 1)]
        else:
            pages = [x for x in range(page_no - max_shown // 2, page_no + max_shown // 2 + 1)]

        context.update({'pages': pages})
        return context


class CreateEventViewPrivate(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'private/event_create.html'
    form_class = EventCreateForm
    success_url = reverse_lazy('event:member_event_list')


class EventDetailViewPrivate(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'private/event_view.html'

    def get_context_data(self, **kwargs):
        context = super(EventDetailViewPrivate, self).get_context_data(**kwargs)
        results = Result.objects.filter(event=self.object)
        if results:
            context.update({'results': results})
        return context


class EventUpdateViewPrivate(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'private/event_create.html'
    form_class = EventUpdateForm
    success_url = reverse_lazy('event:member_event_list')


class EventDeleteViewPrivate(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'private/event_delete.html'
    success_url = reverse_lazy('event:member_event_list')


# Private Member Views: Result


class CreateResultViewPrivate(LoginRequiredMixin, CreateView):
    model = Result
    template_name = 'private/result_create.html'
    form_class = ResultCreateForm
    success_url = reverse_lazy('event:member_event_list')


class ResultDetailViewPrivate(LoginRequiredMixin, DetailView):
    model = Result
    template_name = 'private/result_view.html'


class ResultUpdateViewPrivate(LoginRequiredMixin, UpdateView):
    model = Result
    template_name = 'private/result_create.html'
    form_class = ResultUpdateForm
    success_url = reverse_lazy('event:member_event_list')

    def get_form_class(self, **kwargs):
        result = self.object
        if result.personal_record:
            return ResultPersonalCreateForm
        else:
            return super(ResultUpdateViewPrivate, self).get_form_class(**kwargs)

    def get_success_url(self):
        result = self.object
        if result.personal_record:
            # self.success_url = reverse_lazy('event:member_result_view', kwargs={'pk': result.pk})
            profile = result.rowers.first()
            self.success_url = reverse_lazy('team:view_profile', kwargs={'pk': profile.pk})
        return super(ResultUpdateViewPrivate, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = super(ResultUpdateViewPrivate, self).get_context_data(**kwargs)

        allowed_to_edit = False
        if self.request.user.is_staff:
            allowed_to_edit = True
        elif Profile.objects.filter(owner=self.request.user).exists():
            user_owns_profile = self.request.user.profile == self.object.created_by
            # profile_approved = self.object.created_by.status == APPROVED
            allowed_to_edit = user_owns_profile  # and profile_approved
        if not allowed_to_edit:
            messages.warning(self.request, 'You do not have permission to edit %s' % self.object)
            raise PermissionDenied

        return context


class ResultDeleteViewPrivate(LoginRequiredMixin, DeleteView):
    model = Result
    template_name = 'private/result_delete.html'
    success_url = reverse_lazy('event:member_event_list')


@login_required
def view_leaderboard(request):
    template_name = 'private/leader_board.html'
    distance = int(request.GET.get('distance', 2000))
    lightweight = bool(request.GET.get('lightweight', False))

    if lightweight:
        qs = Profile.objects.filter(results_rowed__personal_record=True,
                                    results_rowed__distance=distance,
                                    results_rowed__lightweight=True,
                                    ).values('first_name',
                                             'last_name',
                                             'id',
                                             'results_rowed__lightweight',
                                             ).annotate(pace=Min('results_rowed__pace')).order_by('pace')[:10]
    else:
        qs = Profile.objects.filter(results_rowed__personal_record=True,
                                    results_rowed__distance=distance,
                                    ).values('first_name',
                                             'last_name',
                                             'id',
                                             'results_rowed__lightweight',
                                             ).annotate(pace=Min('results_rowed__pace')).order_by('pace')[:10]

    for i, result in enumerate(qs):
        result['name'] = result['first_name'] + ' ' + result['last_name']
        result['lightweight'] = result['results_rowed__lightweight']
        result['rank'] = i + 1
        total = result['pace'] * distance / 500
        total_minutes, total_seconds = int(total // 60), total % 60
        result['total_time_string'] = '{:02d}:{:06.3f}'.format(total_minutes, total_seconds)
        result['distance'] = distance
        minutes, seconds = int(result['pace'] // 60), result['pace'] % 60
        result['pace_string'] = '{:02d}:{:06.3f}/500m'.format(minutes, seconds)

    context = {'result_list': qs, }
    return render(request, template_name, context)
