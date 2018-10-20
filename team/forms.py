from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import modelform_factory, inlineformset_factory
from .models import Profile, Membership

User = get_user_model()

ProfileForm = modelform_factory(Profile, exclude=('birthday','bio',))

MembershipForm = modelform_factory(Membership, exclude=('',))

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
