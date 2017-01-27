from django import forms
from django.forms import ModelForm, SelectDateWidget, EmailInput,NumberInput,Select, Textarea, FileInput
from .models import Youth
import datetime

class NewMemberForm(ModelForm):
    class Meta:
         model = Youth
         fields = [ 'name',
                    'date_of_birth',
                    'gender',
                    'phone',
                    'email',
                    'address',
                    'guardian_phone' ,
                    'guardian_email',
                    'interests',
                    'skills',
                    'image'
                    ]
         widgets = {
            'date_of_birth': SelectDateWidget(years=range(1970, datetime.date.today().year+10),
                                    attrs={'class' : 'form-group'} ),
            'gender': Select (attrs={'class' : 'form-group'}),
            'email': EmailInput(attrs={'class' : 'form-group'}),
            'guardian_email': EmailInput(attrs={'class' : 'form-group'}),
            'skills': Textarea(attrs={'class' : 'form-group'}),
            'interests': Textarea(attrs={'class' : 'form-group'}),
            'image': FileInput(attrs={'class' : 'form-group'})
        }
