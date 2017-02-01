from django.contrib import admin
from .models import Youth, Event, EventImages

class EventImagesInline(admin.TabularInline):
        model = EventImages
        extra = 10

class EventAdmin(admin.ModelAdmin):
    inlines = [EventImagesInline]

admin.site.register(Youth)
admin.site.register(Event, EventAdmin)
