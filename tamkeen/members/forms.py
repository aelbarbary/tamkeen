from django import forms
from django.forms import ModelForm, SelectDateWidget, EmailInput,NumberInput
from .models import Youth
import datetime

class NewMemberForm(ModelForm):
    class Meta:
         model = Youth
         fields = ['name', 'date_of_birth', 'phone', 'email']
         widgets = {
            'phone' : NumberInput()
            'date_of_birth': SelectDateWidget(years=range(1970, datetime.date.today().year+10)),
            'email': EmailInput()
        }
