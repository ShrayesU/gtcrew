from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import is_safe_url

from feedback.forms import FeedbackCreateForm
from rowingcrm.settings import ALLOWED_HOSTS


def feedback_submission(request):
    next_url = request.POST.get('next')
    if request.method == 'POST' and request.user.is_authenticated:
        form = FeedbackCreateForm(request.POST)
        if form.is_valid():
            messages.info(request, 'Your feedback has been submitted.')
            form.save()
    if is_safe_url(next_url, allowed_hosts=ALLOWED_HOSTS):
        return redirect(next_url)
    else:
        return redirect(reverse_lazy('team:index_member'))
