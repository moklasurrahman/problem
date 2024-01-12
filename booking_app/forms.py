from email.policy import default
from django.forms import ModelForm, Form, CharField, BooleanField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm


class ProfileChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]

class VerifyForm(Form):
    code = CharField(max_length=8, required=True, help_text='Enter code')

class ReSendCode(Form):
    pass


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add your custom email validation logic here
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('User with same email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # For example, check if the username already exists
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError('A user with that username already exists.')
        return username

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)
        user.save()
        return user

