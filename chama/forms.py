from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Member


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.widgets.TextInput(
        attrs={'placeholder': 'Firstname'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.widgets.TextInput(
        attrs={'placeholder': 'Lastname'}))
    email = forms.EmailField(max_length=254, widget=forms.widgets.EmailInput(
        attrs={'placeholder': 'e.g user@example.com'}))
    phone_number = forms.CharField(max_length=10, required=True, widget=forms.widgets.TextInput(
        attrs={'placeholder': 'e.g 0712345678'}))

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'email',
                  'phone_number', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    pass
