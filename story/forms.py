from django import forms

from common.forms import BaseForm
from .models import Story


class StoryCreateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('date_added', 'created_by',)
        # widgets = {
        #     'profiles_mentioned': autocomplete.ModelSelect2(url='profile:profile_autocomplete')
        # }


class StoryUpdateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('date_added', 'created_by',)
        # widgets = {
        #     'profiles_mentioned': autocomplete.ModelSelect2(url='profile:profile_autocomplete')
        # }
