from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Youth, Event, EventImages
from django.urls import reverse
from django.conf import settings
import datetime
from .forms import NewMemberForm
import logging

def index(request):

    event_list = Event.objects.filter(date_time__gte=datetime.date.today()).order_by('date_time')[:5]
    gallery_list = Event.objects.filter(date_time__lt=datetime.date.today()).order_by('date_time')[:5]
    for gal in gallery_list:
        event_image = EventImages.objects.filter(event = gal.id)
        print(len(event_image))
        gal.image = gal.flyer if len(event_image) == 0 else event_image[0].image
        event_date = gal.date_time.replace(tzinfo=None)
        gal.since = (datetime.datetime.utcnow() - event_date).days

    context = {'event_list': event_list,
                'gallery_list': gallery_list}
    return render(request, 'index.html', context)

def new_member(request):
    if request.method == 'POST':
        print(request.FILES)
        # create a form instance and populate it with data from the request:
        form = NewMemberForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thanks/')

    else:
        form = NewMemberForm()

    return render(request, 'join.html', {'form': form})

def thanks(request):
    return render(request, 'thanks.html', {})

def gallery(request, event_id):
    event_images = EventImages.objects.filter(event = event_id)
    context = {'event_images': event_images}
    return render(request, 'gallery.html', context)
