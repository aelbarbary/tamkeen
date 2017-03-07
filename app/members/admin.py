from django.contrib import admin
from .models import Youth, Event, EventImages, Question, QuestionAnswer, Khatirah, KhatirahAnswer
from .forms import EventForm

class EventImagesInline(admin.TabularInline):
        model = EventImages
        extra = 10

class EventAdmin(admin.ModelAdmin):
    inlines = [EventImagesInline]
    form = EventForm
    class Media:
        css = {
             'all': ('css/eventadmin.css',)
        }

class QuestionAnswersInline(admin.TabularInline):
        model = QuestionAnswer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionAnswersInline]


class KhatirahAnswersInline(admin.TabularInline):
        model = KhatirahAnswer

class KhatirahAdmin(admin.ModelAdmin):
    inlines = [KhatirahAnswersInline]


admin.site.register(Youth)
admin.site.register(Event, EventAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Khatirah, KhatirahAdmin)
