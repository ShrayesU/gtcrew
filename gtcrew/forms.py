from captcha.widgets import ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField
from allauth.account.forms import SignupForm


class AllauthSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def save(self, request):
        user = super(AllauthSignupForm, self).save(request)
        return user
