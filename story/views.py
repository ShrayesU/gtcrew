from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from story.forms import StoryCreateForm, StoryUpdateForm
from story.models import Story


class StoryListView(LoginRequiredMixin, ListView):
    model = Story
    template_name = 'stories.html'
    paginate_by = 10
    ordering = ['-date_added', ]


class CreateStoryView(LoginRequiredMixin, CreateView):
    model = Story
    template_name = 'story_create.html'
    form_class = StoryCreateForm
    success_url = reverse_lazy('story:list')


class StoryDetailView(LoginRequiredMixin, DetailView):
    model = Story
    template_name = 'story_view.html'


class StoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Story
    template_name = 'story_create.html'
    form_class = StoryUpdateForm
    success_url = reverse_lazy('story:list')


class StoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Story
    template_name = 'story_delete.html'
    success_url = reverse_lazy('story:list')
