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

    def get_context_data(self, **kwargs):
        context = super(StoryListView, self).get_context_data(**kwargs)
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
