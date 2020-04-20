from dal import autocomplete
from django import forms
from django_summernote.widgets import SummernoteWidget

from common.forms import BaseForm
from .models import Event, Result


class EventCreateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('date_added', 'date_updated', 'public', 'created_by', 'last_modified_by')
        widgets = {
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', }})
        }


class EventUpdateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('date_added', 'date_updated')
        widgets = {
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', }})
        }


class ResultCreateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Result
        exclude = ('created_by', 'last_modified_by', 'public', 'time')  # TODO: remove time after deleting field
        widgets = {
            'coxswain': autocomplete.ModelSelect2(url='team:profile_autocomplete'),
            'rowers': autocomplete.ModelSelect2Multiple(url='team:profile_autocomplete')
        }


class ResultUpdateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Result
        exclude = ('created_by', 'last_modified_by', 'public', 'time')
        widgets = {
            'coxswain': autocomplete.ModelSelect2(url='team:profile_autocomplete'),
            'rowers': autocomplete.ModelSelect2Multiple(url='team:profile_autocomplete')
        }
