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
from .common_view import *

@staff_member_required
def api_attendance_sheet(request, date):
    result = []
    with connection.cursor() as cursor:
        query = """select p.id, p.first_name, p.last_name, p.gender, a.date_time checkin_time, ch.date_time checkout_time
                from members_profile p
                left join members_attendance a
	            on p.id = a.user_id 
                and a.date_time >= date_trunc('day', to_date(%s, 'YYYYMMDD'))
	            and a.date_time < date_trunc('day', to_date(%s, 'YYYYMMDD') + 1)
                left join members_checkout ch
                on p.id = ch.user_id
                and ch.date_time >= date_trunc('day', to_date(%s, 'YYYYMMDD'))
	            and ch.date_time < date_trunc('day', to_date(%s, 'YYYYMMDD') + 1)
                order by p.first_name"""

        cursor.execute(query, [date,date, date, date])

        for row in cursor.fetchall():
            result.append(json_attendance(row))

        query = "select round((count(*) )::decimal / (select count(*) from members_profile)::decimal * 100,2 ) as f "\
                + "from members_attendance "\
                + "where date_time >= date_trunc('day', to_date(%s, 'YYYYMMDD')) "\
                + "and date_time < date_trunc('day', to_date(%s, 'YYYYMMDD') + 1) "

        cursor.execute(query, [date,date])
        row = cursor.fetchone()

    context = { 'result': result, 'attendance_perc': str(row[0]) }

    data = json.dumps(context)

    return HttpResponse(data, content_type='application/json')

def json_attendance(attendance):

     checked_in = False
     checked_out = False
     checked_in_time = "N/A"
     checked_out_time = "N/A"

     if attendance[4] is not None:
         checked_in = True
         checked_in_time = attendance[4].astimezone(timezone('US/Pacific')).strftime('%-H:%M:%S')

     if attendance[5] is not None:
         checked_out = True
         checked_out_time = attendance[5].astimezone(timezone('US/Pacific')).strftime('%-H:%M:%S')

     return {
         'id': attendance[0],
         'first_name': attendance[1],
         'last_name': attendance[2],
         'gender': attendance[3],
         'checked_in_time': checked_in_time,
         'checked_out_time': checked_out_time,
         'checked_in': checked_in,
         'checked_out': checked_out,
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
def api_checkin(request):
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

@csrf_exempt
@login_required
def api_checkout(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        user_id = json_data["userId"]
        date = json_data["date"]
        date = datetime.strptime(date,'%Y%m%d %H:%M:%S')

        request = Checkout(user_id=user_id, date_time = date )
        request.save()

        return HttpResponse("done")
    else:
        return HttpResponse()

@staff_member_required
def absent(request, period_in_days):
    context = {}
    with connection.cursor() as cursor:

        query = """
            select * from members_profile p
            left  join members_attendance a
             on a.user_id = p.id
             and a.date_time >= NOW() - interval '%s day'
            where a.date_time is null
            ORDER BY first_name, last_name
        """ % period_in_days

        cursor.execute(query)
        absent = dictfetchall(cursor)

        context = { 'absent': absent, 'absent_days': period_in_days }

    return render(request, 'absent.html', context)
