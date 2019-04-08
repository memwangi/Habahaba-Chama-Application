from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Member, Chama, Transaction

from django.utils.translation import ugettext_lazy as _


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.widgets.TextInput(
        attrs={'placeholder': 'Firstname'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.widgets.TextInput(
        attrs={'placeholder': 'Lastname'}))
    email = forms.EmailField(max_length=254, widget=forms.widgets.EmailInput(
        attrs={'placeholder': 'e.g user@example.com'}))
    phone_number = forms.CharField(max_length=10, required=True, widget=forms.widgets.TextInput(
        attrs={'placeholder': 'e.g 0712345678', 'type': 'tel'}))

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'email',
                  'phone_number', 'password1', 'password2')


class CreateChamaForm(ModelForm):

    class Meta:
        model = Chama
        fields = ('groupName', 'paybillNo',
                  'contribution_amnt', 'contribution_interval')
        labels = {'groupName': _('Group Name'),
                  'paybillNo': _('M-Pesa Paybill Number'),
                  'contribution_amnt': _('Contribution Amount'),
                  'contribution_interval': _('Contribution Interval')
                  }
        help_texts = {'groupName': _('e.g Mapato Investment Group'),
                      'paybillNo': _('e.g 568942'),
                      'contribution_amnt': _('Amount member should contribute at a time'),
                      'contribution_interval': _('Number of times contributions are sent in a month e.g 2')
                      }


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('amount','transaction_type')
        labels = {'amount': _('Enter Amount:'),
                  'transaction_type': _('Payment Type')
                  }

class AddMemberForm(forms.Form):
    phone = forms.CharField(max_length=30, required=True, widget=forms.widgets.TextInput(
        attrs={'placeholder': 'Enter Phone Number'}))