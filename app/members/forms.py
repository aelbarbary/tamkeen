from django import forms
from django.forms import ModelForm, SelectDateWidget, EmailInput,NumberInput,Select, Textarea, FileInput
from .models import *
import datetime
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget

class QuestionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput)

class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

class QuizForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput({'size': '40'}))

class EventForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput({'size': '40'}))

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = []
        widgets = {
            'answer': forms.Textarea()
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude=[]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = []

class BookReserveForm(forms.ModelForm):
    class Meta:
        model = BookReserve
        exclude = []

class NewMemberRequestForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = NewMemberRequest
        exclude=[]
        label={
            'phone': 'Phone'
        }

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        exclude = []

class EventParticipantForm(ModelForm):

    class Meta:
        model = EventParticipant
        exclude = []


EventParticipantsFormSet = inlineformset_factory(EventRegistration, EventParticipant, form=EventParticipantForm, extra=6)

MAX_CHILDREN = 5
