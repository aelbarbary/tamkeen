from django import forms
from django.forms import ModelForm, SelectDateWidget, EmailInput,NumberInput,Select, Textarea, FileInput
from .models import Parent, QuestionAnswer, Child, Event
import datetime
from registration.forms import RegistrationForm
from django.forms.models import inlineformset_factory


class EventForm(forms.ModelForm):
    class Meta:
            model = Event
            fields = '__all__'
    BoyGirl_CHOICES = ((0, 'Boy'), (1, 'Girl'))
    gender = forms.TypedChoiceField(
                     choices=BoyGirl_CHOICES, widget=forms.RadioSelect, coerce=int, initial='Boy',
                )

class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

class QuestionAnswerForm(forms.ModelForm):
    answer = forms.CharField(widget=forms.Textarea)

MAX_CHILDREN = 5

class ParentForm(RegistrationForm):
    class Meta:
        model = Parent
        exclude = ['password', 'last_login', 'is_superuser', 'user_permissions', 'groups','is_staff', 'date_joined', 'is_active']

ChildrenFormSet = inlineformset_factory(Parent,
    Child,
    can_delete=False,
    fields = '__all__',
    widgets={
    'date_of_birth': forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                })})
