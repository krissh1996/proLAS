from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
#from .models import LASFile


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'border-gradient', 'name': 'username', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'border-gradient', 'name': 'password', 'placeholder': 'Password'}))


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='', required=True, widget=forms.TextInput(
        attrs={'class': 'border-gradient', 'placeholder': 'First_Name'}))
    last_name = forms.CharField(label='',
                                widget=forms.TextInput(attrs={'class': 'border-gradient', 'placeholder': 'Last_Name'}))
    username = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'class': 'border-gradient', 'placeholder': 'UserName'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'border-gradient', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'border-gradient', 'placeholder': 'Re-Enter Password'}))
    email = forms.EmailField(label='',
                             widget=forms.EmailInput(attrs={'class': 'border-gradient', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            "Email Already Exists")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username has been Taken, Try other one")

    def clean_password(self):
        password = self.cleaned_data['password1']
        if len(password) < 8:
            raise forms.ValidationError('Password too short')
        return super(RegistrationForm, self).clean_password()

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and self.cleaned_data['password1'] != \
                self.cleaned_data['password2']:
            raise forms.ValidationError("The password does not match")
        return self.cleaned_data




