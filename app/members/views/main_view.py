from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from members.models import *
from django.urls import reverse
from django.conf import settings
import logging
from django.db.models import Max, Sum, Count
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from members.forms import *
from django.contrib.auth.decorators import login_required
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.db.models import Q
import os
import logging
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, render_to_response
from members.email import EmailSender
from datetime import date, datetime, timedelta, time
from pytz import timezone
from django.db import connection
from django.contrib.auth import logout
from django.db import transaction

def index(request):
    video_list = []
    videos = SuggestedVideo.objects.all().order_by('-date_time')[0:2]

    context = { 'user_text': request.user if request.user.is_authenticated else 'login', 'videos': videos}
    return render(request, 'index.html', context)

class InquiryCreate(CreateView):
    success_url = '/'
    template_name = 'open-your-heart.html'
    model = Inquiry
    fields = ['name', 'email', 'text']
    def form_valid(self, form):
        response = super(InquiryCreate, self).form_valid(form)
        instance = self.object

        subject = 'Open Your Heart: New Message'
        recepients = [ 'm.h.ali@hotmail.com', 'tamkeen.moderator@gmail.com']
        name = "Anonymous"
        if instance.name:
            name = instance.name
        message = "Name: %s\n" % (name)
        message += "Inquiry: %s\n" % instance.text

        EmailSender(instance, subject, message, recepients).start()
        return render_to_response( 'thanks.html')

def get_videos(request):
    video_list = []
    videos =   SuggestedVideo.objects.all().order_by('-date_time')
    context = { 'videos': videos}
    return render(request, 'view-videos.html', context)

def get_events(request):
    events = Event.objects.all().order_by('-date_time')
    request.session['fav_color'] = 'green'
    context = { 'events': events}
    return render(request, 'view-events.html', context)

class EventRegistration(CreateView):
    success_url = '/'
    template_name = 'events-thank-you.html'
    model = EventRegistration
    fields = ['family_id', 'family_name', 'event']


    def get_context_data(self, **kwargs):
        data = super(EventRegistration, self).get_context_data(**kwargs)
        if self.request.POST:
            data['eventparticipants'] = EventParticipantsFormSet(self.request.POST)
        else:
            data['eventparticipants'] = EventParticipantsFormSet()
        return data


    def form_valid(self, form):

        context = self.get_context_data()
        
        eventparticipants = context['eventparticipants']
        print("eventparticipants %s:" % eventparticipants )
        with transaction.atomic():
            self.object = form.save()
            print("is valid %s: " % eventparticipants.is_valid())
            if eventparticipants.is_valid():
                print("is valid")
                eventparticipants.instance = self.object
                eventparticipants.save()

        response = super(EventRegistration, self).form_valid(form)
        instance = self.object
        subject = 'Event Registration'
        recepients = [ 'abdelrahman.elbarbary@gmail.com']
        name = "Anonymous"
        if instance.family_name:
            name = instance.family_name
        message = "Name: %s\n" % (name)
        EmailSender(instance, subject, message, recepients).start()


        return render_to_response( 'event-thanks2.html')

@csrf_exempt
def play_video(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        video_id = json_data["videoId"]

        video = SuggestedVideo.objects.get(pk=video_id)
        video.views += 1
        video.save()
        return HttpResponse("done")
    else:
        return HttpResponse()

def logout_view(request):
    logout(request)
    return redirect('/')

def competition(request):
    return render(request, "competition.html")
