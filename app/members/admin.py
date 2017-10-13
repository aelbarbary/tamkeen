from django.contrib import admin
from .models import  *
from .forms import QuestionForm, AnswerForm, QuizForm, ProfileForm

admin.site.site_header = 'TAMKEEN admin'

class AnswersInline(admin.TabularInline):
        model = Answer
        form = AnswerForm

class QuestionsInline(admin.TabularInline):
        model = Question
        form = QuestionForm
        inlines = [AnswersInline]
        show_change_link = True

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionsInline]
    form = QuizForm

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswersInline]
    form = QuestionForm

class AnswerAdmin(admin.ModelAdmin):
    form = AnswerForm

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Profile, ProfileAdmin)
