from dal import autocomplete
from django import forms
from django_summernote.widgets import SummernoteWidget

from common.forms import BaseForm
from .models import Story


class StoryCreateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('date_added', 'slug', 'created_by')
        widgets = {
            'story': SummernoteWidget(),
            'profiles_mentioned': autocomplete.ModelSelect2Multiple(url='team:profile_autocomplete')
        }


class StoryUpdateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('date_added', 'slug', 'created_by')
        widgets = {
            'story': SummernoteWidget(),
            'profiles_mentioned': autocomplete.ModelSelect2Multiple(url='team:profile_autocomplete')
        }
