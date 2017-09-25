from django.contrib import admin
from .models import  Question, QuestionAnswer
from .forms import QuestionForm, AnswerQuestionForm

admin.site.site_header = 'TAMKEEN admin'


class QuestionAnswersInline(admin.TabularInline):
        model = QuestionAnswer
        form = AnswerQuestionForm

class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionAnswersInline]
    form = QuestionForm

class QuestionAnswerAdmin(admin.ModelAdmin):
    form = AnswerQuestionForm

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
