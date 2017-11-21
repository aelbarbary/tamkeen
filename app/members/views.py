from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from django.urls import reverse
from django.conf import settings
import logging
from django.db.models import Max, Sum, Count
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from .forms import *
from django.contrib.auth.decorators import login_required
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.db.models import Q
import os
import watchtower
import logging
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, render_to_response
from .email import EmailSender
from datetime import date, datetime, timedelta, time
from pytz import timezone
from django.db import connection
from embed_video.backends import detect_backend

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("django")

def index(request):
    if request.user.is_authenticated:
        name = "%s %s" % (request.user.first_name, request.user.last_name)
        logger.info("user %s has logged" % name)

    video_list = []
    videos =   SuggestedVideo.objects.all().order_by('-date_time')[0:2]
    for v in videos:
        video_list.append(v.video)

    context = { 'user_text': request.user if request.user.is_authenticated else 'login', 'videos': video_list}
    return render(request, 'index.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
@login_required
def quiz(request):
    user_id = request.user.id

    if request.method == 'POST':
        quiz_id = request.POST.get('quiz-id')

        quiz = Quiz.objects.get(pk=quiz_id)
        questions = quiz.questions.all()
        for q in questions:
            answer_text =  request.POST.get('answer-' + str(q.id))
            answer = Answer(text=answer_text, date_time = datetime.now(), score = 0, question_id = q.id, user_id = user_id )
            answer.save()

        return render(request, 'quiz-thanks.html')
    else:
        quizs = Quiz.objects.order_by('-id')[:1]
        if quizs:
            last_quiz = quizs[0]
            questions = last_quiz.questions.all().order_by("id")

            answers = Answer.objects.filter(question_id__in=questions).filter(user_id = user_id )
            if answers:

                    return render(request, 'quiz-thanks.html')
            else:
                context = {'quiz': last_quiz, 'questions': questions }
                return render(request, 'quiz.html', context)

def thanks(request):
    return render(request, 'thanks.html', {})

def registration_activate(request, key):
    return render(request, 'thanks.html', {})

@staff_member_required
def members(request):
    members = Profile.objects.order_by('first_name', 'last_name')
    data = json.dumps([member.json for member in members])
    return HttpResponse(data, content_type='application/json')

@staff_member_required
def show_members(request):
    return render(request, 'view-members.html')

def books(request):
    result = []
    with connection.cursor() as cursor:
        query = "select b.id,b.name, b.description, '/media/' || b.cover_page cover_page, b.category, b.status, b.number_of_pages, '/media/' ||  b.book_file book_file, b.page_num, b.language, b.hardcopy_available, count(r) holds from members_book b "\
                +"left join members_bookreserve r "\
	            +" on b.id = r.book_id "\
                + " group by b.id, b.name"

        cursor.execute(query, [date,date])
        rows = dictfetchall(cursor)
        for row in rows:
            print(row)
            result.append(Book.json(row))

        data = json.dumps(result)

        return HttpResponse(data, content_type='application/json')

def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def show_books(request):
    return render(request, 'view-books.html')

@csrf_exempt
@login_required
def reserve_book(request, id):
    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        user_id = json_data["userId"]
        book_id = id
        request = BookReserve(user_id=user_id, book_id = book_id, date_time = datetime.now() )
        request.save()
        return HttpResponse("done")
    else:
        return HttpResponse()

@login_required
def profile(request):
    profile = Profile.objects.get(pk=request.user.id)
    if profile.skills:
        skills = profile.skills.split(",")
    else:
        skills = []
    answers_count = Answer.objects.filter(user_id=request.user.id).count()
    awards_count = UserAward.objects.filter(user_id=request.user.id).count()
    context = { 'user': profile, 'skills': skills, 'answers_count': answers_count, 'awards_count': awards_count }
    return render(request, 'profile.html', context )

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {
        'form': form
    })

@staff_member_required
def rest_attendance_sheet(request, date):
    result = []
    with connection.cursor() as cursor:
        query = "select p.id, p.first_name, p.last_name, p.gender, date_time "\
                + "from members_profile p left join members_attendance a "\
	            + "on p.id = a.user_id " \
                + "and date_time >= date_trunc('day', to_date(%s, 'YYYYMMDD')) "\
	            + "and date_time < date_trunc('day', to_date(%s, 'YYYYMMDD') + 1)"\
                + "order by p.first_name"

        cursor.execute(query, [date,date])
        for row in cursor.fetchall():
            result.append(json_attendance(row))

        query = "select round((count(*) )::decimal / (select count(*) from members_profile)::decimal * 100,2 ) as f "\
                + "from members_attendance "\
                + "where date_time >= date_trunc('day', to_date(%s, 'YYYYMMDD')) "\
                + "and date_time < date_trunc('day', to_date(%s, 'YYYYMMDD') + 1) "

        cursor.execute(query, [date,date])
        row = cursor.fetchone()
        print(row[0])

    context = { 'result': result, 'attendance_perc': str(row[0]) }

    data = json.dumps(context)

    return HttpResponse(data, content_type='application/json')

def json_attendance(attendance):

     is_attendant = False
     in_time = "N/A"
     if attendance[4]:
         is_attendant = True
         in_time = attendance[4].astimezone(timezone('US/Pacific')).strftime('%-H:%M:%S')
     return {
     'id': attendance[0],
     'first_name': attendance[1],
     'last_name': attendance[2],
     'gender': attendance[3],
     'datetime': in_time,
     'attendance': is_attendant
     }

def get_attendace(user_id, date):
    today = datetime.strptime(date,'%Y%m%d')
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    attendace = Attendance.objects.filter(user_id=user_id, date_time__lte=today_end, date_time__gte=today_start)
    return attendace

@staff_member_required
def attendance_sheet(request):
    return render(request, 'attendance-sheet.html')

@csrf_exempt
@login_required
def record_attendacne(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        user_id = json_data["userId"]
        checked = json_data["checked"]
        date = json_data["date"]
        print(date)
        date = datetime.strptime(date,'%Y%m%d %H:%M:%S')
        if checked == True:
            request = Attendance(user_id=user_id, date_time = date )
            request.save()
        else:
              datePlusOne = date + timedelta(1)
              start = datetime.combine(date, time())
              end = datetime.combine(datePlusOne, time())
              Attendance.objects.filter(user_id=user_id, date_time__lte=end, date_time__gte=start).delete()
        return HttpResponse("done")
    else:
        return HttpResponse()

class NewMemberRequest(CreateView):
    success_url = '/'
    template_name = 'newmemberrequest_form.html'
    model = NewMemberRequest
    # fields = ['first_name','last_name', 'whats_app', 'email', 'gender']
    form_class = NewMemberRequestForm
    # form_class = NewMemberRequestForm
    def form_valid(self, form):
        response = super(NewMemberRequest, self).form_valid(form)
        instance = self.object

        subject = 'New Member Request'
        recepients = ['abdelrahman.elbarbary@gmail.com']

        message = "Tamkeener: %s %s\n" % (instance.first_name, instance.last_name)
        message += "Email: %s\n" % instance.email
        message += "WhatsApp: %s" % instance.whats_app
        EmailSender(instance, subject, message, recepients).start()
        return response

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
    videos =   SuggestedVideo.objects.all()
    for v in videos:
        video_list.append(v.video)

    context = { 'videos': video_list}
    return render(request, 'view-videos.html', context)
