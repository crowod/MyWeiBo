from django import forms


class ProfileForm(forms.Form):
    email_profile = forms.EmailField(required=True,
                                     widget=forms.TextInput(attrs={'class': 'password_input',
                                                                   'placeholder': 'New email address'}),
                                     error_messages={'required': u'Email cannot be null',
                                                     'invalid': u'enter a valid email address.'},)
    password_profile_old = forms.CharField(required=True,
                                           min_length=6,
                                           widget=forms.PasswordInput(attrs={'placeholder': 'Old password'}))
    password_profile_new = forms.CharField(required=True,
                                           min_length=6,
                                           widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    password_cfm_profile_new = forms.CharField(required=True,
                                               min_length=6,
                                               widget=forms.PasswordInput(attrs={'placeholder': 'New password confirmation'}))

    def clean_email_profile(self):
        email = self.cleaned_data['email_profile']

        # raise forms.ValidationError('email already taken.')
        return email

    def clean_password_profile_old(self):
        password_old = self.cleaned_data['password_profile_old']
        # here
        # check whether the old password is correct.
        # raise forms.ValidationError('invalid password.')
        return password_old

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

