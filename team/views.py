import operator
from functools import reduce

from dal import autocomplete
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import (SignUpForm, InterestForm, ProfileUpdateForm, MembershipInlineForm, MembershipUpdateForm,
                    AwardInlineForm)
from .models import Profile, EmailAddress, Page, Post, Membership, AwardGiven, Award
from .utils import APPROVED, UNCLAIMED, PENDING


def page_view(request, page_name):
    page = get_object_or_404(Page, page=page_name)
    pages = Page.objects.all().order_by('sequence')
    posts = Post.objects.filter(page=page).order_by('date_created')
    form = interest(request)
    payload = {
        'page': page,
        'pages': pages,
        'posts': posts,
        'students': None,
        'coaches': None,
    }
    if page.template == 'TEAM':
        students = Membership.students.active()
        coaches = Membership.coaches.active()
        if students:
            payload['students'] = students
            payload['officers'] = students.filter(title__held_by='student').order_by('title__sequence')
        if coaches:
            payload['coaches'] = coaches.order_by('title__sequence')
    return render(request, 'team/page.html', payload)


def home_view(request):
    page_name = Page.objects.all().order_by('sequence')[0].page
    return page_view(request, page_name)


class IndexView(ListView):
    model = Membership
    template_name = 'team/membership_index.html'
    context_object_name = 'membership_list'

    def get_queryset(self):
        return Membership.students.active().order_by('squad')


class MembershipDetail(DetailView):
    model = Membership
    template_name = 'team/membership_detail.html'


def signup(request):
    success_url = reverse_lazy('team:list_profile')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect(success_url)

    else:
        form = SignUpForm()
    return render(request, 'team/register.html', {'form': form})


def interest(request):
    pages = Page.objects.all().order_by('sequence')
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            gtid = form.cleaned_data.get('gtid')
            p = Profile(
                first_name=first_name,
                last_name=last_name,
                gtid=gtid,
            )
            p.save()
            e, e_saved = EmailAddress.objects.get_or_create(
                email=email,
                profile=p,
            )
            return redirect('')
    else:
        form = InterestForm()
    return render(request, 'team/interest.html', {'form': form, 'pages': pages})


"""
Profile Views
"""


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profile/profiles.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
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


def manage_awards(request, profile_id):
    template_name = 'profile/manage_related.html'
    profile = get_object_or_404(Profile, pk=profile_id)
    inline_form = AwardInlineForm
    prefix = 'awardgiven_set'
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
        if formset.is_valid():
            formset.save()
            return redirect(success_url)
    else:
        formset = inline_form(instance=profile)

    return render(request, template_name, {'formset': formset, 'profile': profile, 'prefix': prefix})


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


"""
Award Views
"""


class AwardGivenDetailView(LoginRequiredMixin, DetailView):
    model = AwardGiven
    template_name = 'award/awardgiven_view.html'


class AwardDetailView(LoginRequiredMixin, ListView):
    model = AwardGiven
    template_name = 'award/award_view.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(AwardDetailView, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            context['award'] = get_object_or_404(Award, id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        award = get_object_or_404(Award, id=self.kwargs['pk'])
        return AwardGiven.objects.filter(award=award)


class AwardListView(LoginRequiredMixin, ListView):
    model = Award
    template_name = 'award/awards.html'
    paginate_by = 5


"""
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birthday = form.cleaned_data.get('birthday')
            user.profile.major = form.cleaned_data.get('major')
            user.profile.hometown = form.cleaned_data.get('hometown')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('')
    else:
        form = SignUpForm()
    return render(request, 'team/includes/signup.html', {'form': form})
"""
"""
from django.core.mail import send_mail
from .forms import ContactForm
def get_contact(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
"""
