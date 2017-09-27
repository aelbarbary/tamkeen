from django import forms
from django.forms import ModelForm, SelectDateWidget, EmailInput,NumberInput,Select, Textarea, FileInput
from .models import Answer
import datetime
from registration.forms import RegistrationForm
from django.forms.models import inlineformset_factory

class QuestionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput)

class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

class QuizForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput({'size': '40'}))

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        exclude = []
        widgets = {
            'answer': forms.Textarea()

        }

MAX_CHILDREN = 5
