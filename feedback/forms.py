from django import forms

from common.forms import BaseForm
from .models import Feedback


class FeedbackCreateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('feedback', )

    def __init__(self, *args, **kwargs):
        super(FeedbackCreateForm, self).__init__(*args, **kwargs)
        self.fields['feedback'].widget.attrs['placeholder'] = 'Thanks Champ...'
