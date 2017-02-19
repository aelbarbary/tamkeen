from django.contrib import admin
from .models import Youth, Event, EventImages
from .forms import EventForm

class EventImagesInline(admin.TabularInline):
        model = EventImages
        extra = 10

class EventAdmin(admin.ModelAdmin):
    inlines = [EventImagesInline]

class EventAdmin(admin.ModelAdmin):
    form = EventForm
    class Media:
        css = {
             'all': ('css/eventadmin.css',)
        }

admin.site.register(Youth)
admin.site.register(Event, EventAdmin)
