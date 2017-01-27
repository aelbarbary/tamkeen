from django import forms
from django.forms import ModelForm, SelectDateWidget, EmailInput,NumberInput, Select, Textarea
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
            'gender': Select (),
            'email': EmailInput(),
            'guardian_email': EmailInput(),
            'skills': Textarea(),
            'interests': Textarea()
        }
