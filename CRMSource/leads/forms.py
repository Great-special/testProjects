from django import forms
from . import models



class LeadForm(forms.ModelForm):
    # name = forms.CharField()
    # account_name = forms.CharField()
    # contact_name = forms.CharField()
    # email = forms.EmailField()
    # phone = forms.CharField()
   
    class Meta:
        model = models.Lead
        fields = [
            "title",
            "account_name",
            "contact_name",
            "email",
            "phone",
            "manager"
        ]

