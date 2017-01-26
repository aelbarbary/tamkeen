from django import forms
from django.forms import ModelForm
from .models import Youth

class NewMemberForm(ModelForm):
    class Meta:
         model = Youth
         fields = ['name', 'date_of_birth', 'phone', 'email']
