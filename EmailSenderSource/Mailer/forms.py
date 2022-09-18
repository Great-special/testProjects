from django import forms
from . import models

class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = "__all__"


class EmailsForm(forms.ModelForm):
    class Meta:
        model = models.EMails
        fields = ['email']