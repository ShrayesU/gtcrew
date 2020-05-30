from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView

from actstream import action
from common.views import PagesListView, RequireProfileExistsUpdateView, RequireProfileExistsMixin
from .forms import AssetCreateForm, AssetUpdateForm
from .models import Asset
from .utils import SHELL


class AssetListView(LoginRequiredMixin, RequireProfileExistsMixin, PagesListView):
    model = Asset
    template_name = 'assets.html'
    paginate_by = 10


class CreateAssetView(LoginRequiredMixin, RequireProfileExistsMixin, CreateView):
    model = Asset
    template_name = 'asset_create.html'
    form_class = AssetCreateForm
    success_url = reverse_lazy('asset:list')

    def get_success_url(self):
        if self.object.type == SHELL:
            verb = 'created {}'.format(self.object.get_type_display())
            action.send(self.request.user.profile, verb=verb, action_object=self.object)
        return super(CreateAssetView, self).get_success_url()


class AssetDetailView(LoginRequiredMixin, RequireProfileExistsMixin, DetailView):
    model = Asset
    template_name = 'asset_view.html'


class AssetUpdateView(LoginRequiredMixin, RequireProfileExistsUpdateView):
    model = Asset
    template_name = 'asset_create.html'
    form_class = AssetUpdateForm
    success_url = reverse_lazy('asset:list')

    def get_success_url(self):
        if self.object.type == SHELL:
            verb = 'updated {}'.format(self.object.get_type_display())
            action.send(self.request.user.profile, verb=verb, action_object=self.object)
        return super(AssetUpdateView, self).get_success_url()


class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = 'asset_delete.html'
    success_url = reverse_lazy('asset:list')
