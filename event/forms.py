from dal import autocomplete
from django import forms
from django_summernote.widgets import SummernoteWidget
from tempus_dominus.widgets import DateTimePicker, DatePicker

from common.forms import BaseForm
from .models import Event, Result


class EventCreateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('date_added', 'date_updated', 'public', 'created_by', 'last_modified_by')
        widgets = {
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', }}),
            'start_datetime': DateTimePicker(options={
                'icons': {'time': "fa fa-clock"},
            }),
            'end_datetime': DateTimePicker(options={
                'icons': {'time': "fa fa-clock"},
            }),
        }


class EventUpdateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('date_added', 'date_updated', 'public', 'created_by', 'last_modified_by')
        widgets = {
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', }}),
            'start_datetime': DateTimePicker(options={
                'icons': {'time': "fa fa-clock"},
            }),
            'end_datetime': DateTimePicker(options={
                'icons': {'time': "fa fa-clock"},
            }),
        }


class ResultCreateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Result
        exclude = (
            'created_by', 'last_modified_by', 'public', 'personal_record', 'pace')
        widgets = {
            'coxswain': autocomplete.ModelSelect2(url='team:profile_autocomplete'),
            'rowers': autocomplete.ModelSelect2Multiple(url='team:profile_autocomplete'),
            'date': DatePicker(),
            'event': forms.HiddenInput(),
        }


class ResultUpdateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Result
        exclude = ('created_by', 'last_modified_by', 'public', 'personal_record', 'pace', 'event')
        widgets = {
            'coxswain': autocomplete.ModelSelect2(url='team:profile_autocomplete'),
            'rowers': autocomplete.ModelSelect2Multiple(url='team:profile_autocomplete'),
            'date': DatePicker(),
        }


class ResultPersonalCreateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Result
        fields = ('date', 'distance', 'minutes', 'seconds', 'lightweight')
        widgets = {
            'date': DatePicker(),
        }
