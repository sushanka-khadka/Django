from django import forms
from .models import Participant

class RegistrationForm(forms.Form):     # has no relation with model so will not force unique email, as get_or_create method is used earlier, which will only create if it didn't exist
    email = forms.EmailField()


# class RegistrationForm(forms.ModelForm):    # force form for unique email validation 
#     class Meta:
#         model= Participant
#         fields = ['email']