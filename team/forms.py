from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import modelform_factory, inlineformset_factory
from django.core.validators import RegexValidator
from .models import Profile, Membership

from antispam.captcha.forms import ReCAPTCHA

User = get_user_model()

ProfileForm = modelform_factory(Profile, exclude=('birthday','bio',))

MembershipForm = modelform_factory(Membership, exclude=('',))

class InterestForm(forms.Form):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField(max_length=254)
    gtid = forms.CharField(help_text='Optional. For current GT students.', max_length=9, required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={'width': '100%'}), max_length=200, required=False)
    captcha = ReCAPTCHA()

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    birthday = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    major = forms.CharField(help_text='Optional. College major.', max_length=64, required=False)
    hometown = forms.CharField(help_text='Optional.', max_length=64, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'birthday', 'major', 'hometown', 'password1', 'password2', )
