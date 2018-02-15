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

def index(request):
    video_list = []
    videos =   SuggestedVideo.objects.all().order_by('-date_time')[0:2]

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


@staff_member_required
def stats(request):
    context = {}
    with connection.cursor() as cursor:
        # USer Info completeness
        query = "select round(count(1)::numeric/(select count(1) from members_profile ) ::numeric  ,2) * 100 "\
                + "from members_profile "\
                + "where whats_app <> '' and uw_waiver <> 'uw_waivers/default.png'"

        cursor.execute(query)
        completeness = cursor.fetchone()

        # Quiz answers
        query = "select count(1) " \
                +"from members_answer "\
                +"where date_time > NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7"

        cursor.execute(query)
        quiz_answers = cursor.fetchone()

        # New Members
        query = "select count(1) " \
                +"from members_profile "\
                +"where date_joined > NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7"

        cursor.execute(query)
        new_members = cursor.fetchone()

        # Books checkouts
        query = "select count(1) " \
                +"from members_bookreserve "\
                +"where date_time > NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7"

        cursor.execute(query)
        book_checkouts = cursor.fetchone()

        # Open your heart
        query = "select count(1) " \
                +"from members_inquiry "\
                +"where date_time > NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7"

        cursor.execute(query)
        open_your_heart = cursor.fetchone()

        context = { 'completeness':completeness[0],
                'quiz_answers': quiz_answers[0],
                'new_members': new_members[0],
                'book_checkouts' :book_checkouts[0],
                'open_your_heart': open_your_heart[0]}


    return render(request, 'stats.html', context)

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

@staff_member_required
def alerts(request):
    context = {}
    with connection.cursor() as cursor:
        # Tamkeeners missing for a month
        query = """
            select count(1) from members_profile p
            left  join members_attendance a
             on a.user_id = p.id
             and a.date_time >= NOW() - interval '30 day'
            where a.date_time is null
        """

        cursor.execute(query)
        missing_for_a_month = cursor.fetchone()

        # missing for 2 weeks answers
        query = """
            select count(1) from members_profile p
            left  join members_attendance a
             on a.user_id = p.id
             and a.date_time >= NOW() - interval '14 day'
            where a.date_time is null
        """

        cursor.execute(query)
        missing_for_2_weeks = cursor.fetchone()

        # never showed up
        query = """
            select count(1) from members_profile p
            left  join members_attendance a
             on a.user_id = p.id
              and a.date_time >= NOW() - interval '180 day'
            where a.date_time is null
        """

        cursor.execute(query)
        missing_for_6_month = cursor.fetchone()


        context = { 'missing_for_a_month':missing_for_a_month[0],
                    'missing_for_2_weeks': missing_for_2_weeks[0],
                    'missing_for_6_month': missing_for_6_month[0],
                }


    return render(request, 'alerts.html', context)
