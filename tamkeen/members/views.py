from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Youth, Event
from django.urls import reverse
from django.conf import settings

def index(request):
    youth_list = Youth.objects.order_by('rank')[:6]
    context = {'youth_list': youth_list}
    print (youth_list[0])
    return render(request, 'index.html', context)

# def index(request):
#     youth_list = Youth.objects.order_by('rank')[:10]
#
#     for youth in youth_list:
#         youth.imageurl = youth.image.url[7:]
#
#     context = {'youth_list': youth_list}
#     return render(request, 'index.html', context)

def all_members(request):
    youth_list = Youth.objects.order_by('rank')
    context = {'youth_list': youth_list}
    return render(request, 'all_members.html', context)

def event(request):
    event_list = Event.objects.order_by('name')[:100]
    for event in event_list:
        event.imageurl = event.image.url[7:]

    context = {'event_list': event_list}
    return render(request, 'event.html', context)

def all_events(request):
    event_list = Event.objects.order_by('date_time')[:100]
    for event in event_list:
        event.imageurl = event.image.url[7:]

    context = {'event_list': event_list}
    return render(request, 'all_events.html', context)
