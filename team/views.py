from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import (ProfileForm, InterestForm, ProfileUpdateForm, MembershipInlineForm, MembershipUpdateForm,
                    AwardInlineForm)
from .models import Profile, EmailAddress, Page, Post, Membership, AwardGiven


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


class DetailView(DetailView):
    model = Membership
    template_name = 'team/membership_detail.html'


def signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm()
    return render(request, 'team/includes/signup.html', {'form': form})


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
    paginate_by = 5


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


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile/profile_create.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('team:list_profile')

    def get_success_url(self):
        return reverse_lazy('team:view_profile', kwargs={'pk': self.object.pk})


def manage_memberships(request, profile_id):
    template_name = 'profile/manage_related.html'
    profile = Profile.objects.get(pk=profile_id)
    inline_form = MembershipInlineForm
    prefix = 'membership_set'
    success_url = reverse_lazy('team:view_profile', kwargs={'pk': profile.pk})

    if request.method == "POST":
        formset = inline_form(request.POST, request.FILES, instance=profile)
        if formset.is_valid():
            formset.save()
            return redirect(success_url)
    else:
        formset = inline_form(instance=profile)

    return render(request, template_name, {'formset': formset, 'profile': profile, 'prefix': prefix})


def manage_awards(request, profile_id):
    template_name = 'profile/manage_related.html'
    profile = Profile.objects.get(pk=profile_id)
    inline_form = AwardInlineForm
    prefix = 'awardgiven_set'
    success_url = reverse_lazy('team:view_profile', kwargs={'pk': profile.pk})

    if request.method == "POST":
        formset = inline_form(request.POST, request.FILES, instance=profile)
        if formset.is_valid():
            formset.save()
            return redirect(success_url)
    else:
        formset = inline_form(instance=profile)

    return render(request, template_name, {'formset': formset, 'profile': profile, 'prefix': prefix})


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


class AwardDetailView(LoginRequiredMixin, DetailView):
    model = AwardGiven
    template_name = 'award/award_view.html'


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
