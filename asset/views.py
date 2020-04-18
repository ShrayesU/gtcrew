from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from team.models import Profile
from .forms import AssetCreateForm, AssetUpdateForm
from .models import Asset


class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = 'assets.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(AssetListView, self).get_context_data(**kwargs)

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


class CreateAssetView(LoginRequiredMixin, CreateView):
    model = Asset
    template_name = 'asset_create.html'
    form_class = AssetCreateForm
    success_url = reverse_lazy('asset:list')


class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    template_name = 'asset_view.html'


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    template_name = 'asset_create.html'
    form_class = AssetUpdateForm
    success_url = reverse_lazy('asset:list')

    def get_context_data(self, **kwargs):
        context = super(AssetUpdateView, self).get_context_data(**kwargs)

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


class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = 'asset_delete.html'
    success_url = reverse_lazy('asset:list')
