from django import forms
from django.contrib.auth import get_user_model
from django.forms import modelform_factory, inlineformset_factory
from django_summernote.widgets import SummernoteWidget

from common.forms import BaseForm
from .models import Profile, Membership, AwardGiven

User = get_user_model()

ProfileForm = modelform_factory(Profile, exclude=('bio',))

MembershipInlineForm = inlineformset_factory(Profile, Membership, exclude=('public',), extra=1)

AwardInlineForm = inlineformset_factory(Profile, AwardGiven, exclude=(), extra=1)


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ProfileUpdateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('date_updated', 'date_added', 'owner', 'status', 'public')
        widgets = {
            'bio': SummernoteWidget(attrs={'summernote': {'width': '100%',
                                                          'placeholder': 'Write a little something...'}
                                           }),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['gtid'].widget.attrs['placeholder'] = '90*******'
        self.fields['birthday'].widget.attrs['placeholder'] = 'YYYY-MM-DD'
        self.fields['major'].widget.attrs['placeholder'] = 'Mechanical Engineering'
        self.fields['hometown'].widget.attrs['placeholder'] = 'Atlanta, GA'


class MembershipUpdateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('semester', 'year', 'profile', 'squad', 'title')

    def __init__(self, *args, **kwargs):
        super(MembershipUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['profile'].widget.attrs['style'] = 'display:none;'
