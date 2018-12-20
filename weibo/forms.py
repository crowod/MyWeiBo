import re

from django import forms
from django.core.validators import RegexValidator, validate_email

from weibo.models import User


class LoginForm(forms.Form):
    email_sign_in = forms.CharField(required=True, error_messages={'required': u'Email/Username cannot be null',
                                                                   'invalid': u'enter a valid email/username.'}, )
    password_sign_in = forms.CharField(widget=forms.PasswordInput(), min_length=6, required=True, )

    def clean_email_sign_in(self):
        email = self.cleaned_data['email_sign_in']
        if re.search(r'^([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
            if re.search('[A-Z]+', email):
                raise forms.ValidationError('Enter a valid email address.')
                return email
        elif re.search(r'^[^a-z0-9_-]*$', email):
            raise forms.ValidationError('Enter a valid username.')
            return email

        have_email = User.objects.filter(email=email).count()
        have_username = User.objects.filter(username=email).count()
        if have_email == 0 and have_username == 0:
            raise forms.ValidationError('user not found.')
        return email


class RegisterForm(forms.Form):
    email_sign_up = forms.EmailField(required=True,
                                     error_messages={'required': u'Email cannot be null',
                                                     'invalid': u'enter a valid email address.'}, )

    username_sign_up = forms.CharField(required=True,
                                       validators=[
                                           RegexValidator(
                                               regex=r'^[a-z0-9_-]+$',
                                               message='username has illegal characters.',
                                               code='invalid_username'
                                           ),
                                       ]
                                       )
    password_sign_up = forms.CharField(widget=forms.PasswordInput(), required=True)
    password_cfm_sign_up = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean_email_sign_up(self):
        email = self.cleaned_data['email_sign_up']
        if re.search(r'[A-Z]+', email):
            raise forms.ValidationError('email has illegal characters')
        have_email = User.objects.filter(email=email).count()
        if have_email:
            raise forms.ValidationError('email already taken.')
        return email

    def clean_username_sign_up(self):
        usrname = self.cleaned_data['username_sign_up']
        have_name = User.objects.filter(username=usrname).count()
        if have_name:
            raise forms.ValidationError('username already taken.')
        return usrname

    def clean_password_sign_up(self):
        password = self.cleaned_data['password_sign_up']
        if len(password) < 6:
            raise forms.ValidationError('password too short.')
        return password

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'password_sign_up' in cleaned_data and 'password_cfm_sign_up' in cleaned_data:
            password = cleaned_data['password_sign_up']
            password_cfm = cleaned_data['password_cfm_sign_up']
            if password != password_cfm:
                raise forms.ValidationError('password mismatch.')
        return cleaned_data


user = None


class ProfileForm(forms.Form):
    password_profile_old = forms.CharField(required=True,
                                           min_length=6,
                                           widget=forms.PasswordInput(attrs={'placeholder': 'Your old password'}))
    password_profile_new = forms.CharField(required=True,
                                           min_length=6,
                                           widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    password_cfm_profile_new = forms.CharField(required=True,
                                               min_length=6,
                                               widget=forms.PasswordInput(
                                                   attrs={'placeholder': 'New password confirmation'}))


    def clean_password_profile_new(self):
        password_new = self.cleaned_data['password_profile_new']
        if len(password_new) < 6:
            raise forms.ValidationError('password too short.')
        else:
            return password_new

    def clean_password_cfm_profile_new(self):
        password_new = self.cleaned_data['password_profile_new']
        password_cfm_new = self.cleaned_data['password_cfm_profile_new']
        if password_new != password_cfm_new:
            raise forms.ValidationError('password mismatch.')
        else:
            return password_cfm_new
