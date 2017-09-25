from django import forms
from django.forms import ModelForm, SelectDateWidget, EmailInput,NumberInput,Select, Textarea, FileInput
from .models import QuestionAnswer
import datetime
from registration.forms import RegistrationForm
from django.forms.models import inlineformset_factory

class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

class AnswerQuestionForm(forms.ModelForm):

    class Meta:
        model = QuestionAnswer
        fields = ["answer", "date_time", "score"]
        widgets = {
            'answer': forms.Textarea(),
            'score': forms.HiddenInput()
        }
    # def __init__(self, *args, **kwargs):
    #       super().__init__(*args, **kwargs)
        #   self.fields['question'].label = self.instance.id
        #   self.fields['image'].label = "Icon"
        #   self.fields['description'].label = "How to get there?"

MAX_CHILDREN = 5
