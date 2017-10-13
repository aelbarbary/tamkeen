from django import forms
from django.forms import ModelForm, SelectDateWidget, EmailInput,NumberInput,Select, Textarea, FileInput
from .models import *
import datetime
from registration.forms import RegistrationForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

class QuestionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput)

class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

class QuizForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput({'size': '40'}))

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Profile
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'whats_app',)

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
        exclude = []
        

MAX_CHILDREN = 5
