from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from common.views import PagesListView
from story.forms import StoryCreateForm, StoryUpdateForm
from story.models import Story
from team.models import Profile


class StoryListView(LoginRequiredMixin, PagesListView):
    model = Story
    template_name = 'stories.html'
    paginate_by = 10
    ordering = ['-date_added', ]

    def get_context_data(self, **kwargs):
        context = super(StoryListView, self).get_context_data(**kwargs)

        # include popular and newest stories
        popular_stories = Story.objects.all().order_by('-page_views')[0:3]
        newest_stories = Story.objects.all().order_by('-date_added')[:3]
        context.update({'popular_stories': popular_stories, 'newest_stories': newest_stories})

        return context


class CreateStoryView(LoginRequiredMixin, CreateView):
    model = Story
    template_name = 'story_create.html'
    form_class = StoryCreateForm
    success_url = reverse_lazy('story:list')


class StoryDetailView(LoginRequiredMixin, DetailView):
    model = Story
    template_name = 'story_view.html'

    def get_object(self, queryset=None):
        story = super().get_object(queryset)
        # increments page_views without altering last_modified
        Story.objects.filter(pk=story.pk).update(page_views=F('page_views') + 1)
        return super().get_object(queryset)


class StoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Story
    template_name = 'story_create.html'
    form_class = StoryUpdateForm
    success_url = reverse_lazy('story:list')

    def get_context_data(self, **kwargs):
        context = super(StoryUpdateView, self).get_context_data(**kwargs)

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


class StoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Story
    template_name = 'story_delete.html'
    success_url = reverse_lazy('story:list')
