from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from captcha.fields import ReCaptchaField


class AllauthSignupForm(forms.Form):

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def save(self, request, user):
        user = super(AllauthSignupForm, self).save(request)
        return user
