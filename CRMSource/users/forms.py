from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


# class UserModelForm(forms.ModelForm):
#     confirm_password = forms.CharField()
#     class Meta:
#         model = models.User
#         fields = ['username', 'email', 'password', 'confirm_password']


class UserModelForm(UserCreationForm):
    # email = forms.EmailField()
    class Meta:
        model = models.User
        fields = ['username', 'email', 'password1', 'password2']


class ManagerModelForm(forms.ModelForm):
    is_organisor = forms.BooleanField()
    is_manager = forms.BooleanField()
    class Meta:
        model = models.User
        fields = ['username', 'email', "is_organisor", 'is_manager']

class TeamModelForm(forms.ModelForm):
    # list_ = forms.ModelMultipleChoiceField(models.User.objects.all())
    class Meta:
        model = models.TeamMember
        fields = "__all__"
        
    