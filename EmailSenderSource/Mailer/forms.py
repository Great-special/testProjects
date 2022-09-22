from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models

class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ['subject', 'body', 'receiver','repeat', 'schedule']


class EmailsForm(forms.ModelForm):
    class Meta:
        model = models.EMails
        fields = ['email', 'group']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        