from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic

from django.contrib.auth import login, authenticate
from .forms import SignUpForm, ProfileForm, InterestForm


from .models import Profile, Page, Post, Membership

def PageView(request, pagename):
    page = get_object_or_404(Page, page=pagename)
    pages = Page.objects.all().order_by('sequence')
    posts = Post.objects.filter(page=page)
    form = interest(request)
    payload = {
            'page': page,
            'pages': pages,
            'posts': posts,
            'students': None,
            'coaches': None,
            }
    if page.template == 'TEAM':
        most_recent_member = Membership.objects.order_by('-year', 'semester').first()
        year, semester = (most_recent_member.year, most_recent_member.semester)
        payload['students'] = Membership.objects.filter(year=year, semester=semester).exclude(
                                                            title__held_by='coach'
                                                            ).exclude(
                                                                title__held_by='alumni'
                                                                )
        payload['coaches'] = Membership.objects.filter(year=year, semester=semester, title__held_by='coach')
        payload['officers'] = Membership.objects.filter(year=year, semester=semester, title__held_by='student')
    return render(request, 'team/page.html', payload)
    
def HomeView(request):
    pagename = Page.objects.all().order_by('sequence')[0].page
    return PageView(request, pagename)

class IndexView(generic.ListView):
    model = Membership
    template_name = 'team/membership_index.html'
    context_object_name = 'membership_list'
    
    def get_queryset(self):
        return Membership.objects.all()[:5]

class DetailView(generic.DetailView, pk):
    model = Membership
    template_name = 'team/membership_detail.html'
    
    def get_queryset(self):
        return Membership.objects.get(pk=pk)

def signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm()
    return render(request, 'team/includes/signup.html', {'form':form})

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
                        email=email,
                        gtid=gtid,
                        )
            p.save()
            return redirect('')
    else:
        form = InterestForm()
    return render(request, 'team/interest.html', {'form':form, 'pages':pages})

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
