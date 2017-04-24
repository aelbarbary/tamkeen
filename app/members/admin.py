from django.contrib import admin
from .models import Event,  Question, QuestionAnswer
from .forms import EventForm, QuestionForm, QuestionAnswerForm

admin.site.site_header = 'TAMKEEN admin'

class EventAdmin(admin.ModelAdmin):
    form = EventForm
    class Media:
        css = {
             'all': ('css/eventadmin.css',)
        }

class QuestionAnswersInline(admin.TabularInline):
        model = QuestionAnswer
        form = QuestionAnswerForm

class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionAnswersInline]
    form = QuestionForm

admin.site.register(Event, EventAdmin)
admin.site.register(Question, QuestionAdmin)
