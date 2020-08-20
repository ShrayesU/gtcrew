import operator
from functools import reduce

from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView

from actstream import action
from common.views import PagesListView
from story.models import Story
from .forms import ProfileUpdateForm, MembershipInlineForm, MembershipUpdateForm
from .models import Profile, Membership
from .utils import APPROVED, UNCLAIMED, PENDING

"""
Profile Views
"""


class PortalView(LoginRequiredMixin, TemplateView):
    template_name = 'private.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_count_all'] = Profile.objects.all().count()
        context['profile_count_approved'] = Profile.objects.filter(status=APPROVED).count()
        context['story_count_all'] = Story.objects.all().count()
        membership_list = Membership.objects.values('year', 'semester').annotate(count=Count('profile'))
        context['membership_list'] = membership_list
        context['membership_count'] = [x['count'] for x in membership_list]
        context['membership_label'] = [str('{}{}'.format(x['semester'], x['year'])) for x in membership_list]
        context['profile_model'] = Profile
        return context


"""
Profile Views
"""


class ProfileListView(LoginRequiredMixin, PagesListView):
    model = Profile
    template_name = 'profile/profiles.html'
    paginate_by = 10


class SearchProfileListView(ProfileListView):
    def get_queryset(self):
        result = super(SearchProfileListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(first_name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(last_name__icontains=q) for q in query_list))
            )

        return result


class ProfileAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Profile.objects.none()

        qs = Profile.objects.all()

        if self.q:
            query_list = self.q.split()
            qs = qs.filter(
                reduce(operator.and_,
                       (Q(first_name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(last_name__icontains=q) for q in query_list))
            )

        return qs


class CreateProfileView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Profile
    template_name = 'profile/profile_create.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('team:list_profile')
    success_message = "%(object)s was created successfully"

    def get_success_message(self, cleaned_data):
        if Profile.objects.filter(owner=self.request.user).exists():
            action.send(self.request.user.profile, verb='created profile', action_object=self.object)
        else:
            action.send(self.object, verb='profile was created')
        return self.success_message % dict(
            cleaned_data,
            object=self.object,
        )


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile/profile_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)

        allowed_to_edit = False
        if self.request.user.is_staff:
            allowed_to_edit = True
        elif Profile.objects.filter(owner=self.request.user).exists():
            user_owns_profile = self.request.user.profile == self.object
            profile_approved = self.object.status == APPROVED
            allowed_to_edit = user_owns_profile and profile_approved
        context.update({'allowed_to_edit': allowed_to_edit})

        profile_status = self.object.status
        if profile_status == UNCLAIMED:
            context.update({'profile_status': 'unclaimed'})
        elif profile_status == PENDING:
            context.update({'profile_status': 'pending',
                            'pending_owner': self.object.owner.username, })

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile/profile_create.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('team:list_profile')

    def get_success_url(self):
        action.send(self.request.user.profile, verb='updated profile', action_object=self.object)
        return reverse_lazy('team:view_profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)

        allowed_to_edit = False
        if self.request.user.is_staff:
            allowed_to_edit = True
        elif Profile.objects.filter(owner=self.request.user).exists():
            user_owns_profile = self.request.user.profile == self.object
            profile_approved = self.object.status == APPROVED
            allowed_to_edit = user_owns_profile and profile_approved
        if not allowed_to_edit:
            messages.warning(self.request, 'You do not have permission to edit %s' % self.object)
            raise PermissionDenied

        return context


@login_required
def manage_memberships(request, profile_id):
    template_name = 'profile/manage_related.html'
    profile = get_object_or_404(Profile, pk=profile_id)
    inline_form = MembershipInlineForm
    prefix = 'membership_set'
    success_url = reverse_lazy('team:view_profile', kwargs={'pk': profile.pk})

    allowed_to_edit = False
    if request.user.is_staff:
        allowed_to_edit = True
    elif Profile.objects.filter(owner=request.user).exists():
        user_owns_profile = request.user.profile == profile
        profile_approved = profile.status == APPROVED
        allowed_to_edit = user_owns_profile and profile_approved
    if not allowed_to_edit:
        messages.warning(request, 'You do not have permission to edit %s' % profile)
        raise PermissionDenied

    if request.method == "POST":
        formset = inline_form(request.POST, request.FILES, instance=profile)
        if formset.is_valid() and allowed_to_edit:
            formset.save()
            return redirect(success_url)
    else:
        formset = inline_form(instance=profile)

    context = {'formset': formset, 'profile': profile, 'prefix': prefix, }
    return render(request, template_name, context)


@login_required
def claim_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    success_url = reverse_lazy('team:view_profile', kwargs={'pk': profile.pk})

    if Profile.objects.filter(owner=request.user).exists():
        # user already has a profile
        messages.warning(request, 'Attempt failed. You already have a profile claimed on your account.')
    elif profile.owner:
        # profile already has an owner
        messages.warning(request, 'Attempt failed. This profile already has an owner.')
    else:
        profile.owner = request.user
        profile.status = PENDING
        profile.save()
        messages.success(request, 'You have successfully submitted a claim for this profile.')

    return redirect(success_url)


"""
Membership Views
"""


class MembershipListView(LoginRequiredMixin, ListView):
    model = Membership
    template_name = 'membership/memberships.html'
    paginate_by = 5


class CreateMembershipView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Membership
    template_name = 'membership/membership_create.html'
    form_class = MembershipUpdateForm
    success_url = reverse_lazy('team:list_membership')
    success_message = "%(object)s was created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            object=self.object,
        )


class MembershipDetailView(LoginRequiredMixin, DetailView):
    model = Membership
    template_name = 'membership/membership_view.html'


class MembershipUpdateView(LoginRequiredMixin, UpdateView):
    model = Membership
    template_name = 'membership/membership_create.html'
    form_class = MembershipUpdateForm
    success_url = reverse_lazy('team:list_membership')

    def get_success_url(self):
        return reverse_lazy('team:view_profile', kwargs={'pk': self.object.profile.pk})
