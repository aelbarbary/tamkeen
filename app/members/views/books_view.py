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

def get_books(request):
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

def get_requested_books(request):
    result = []
    with connection.cursor() as cursor:
        query = "select b.id,b.name, b.description, p.first_name, p.last_name "\
                +"from members_book b "\
                +"join  members_bookreserve r "\
                +"on b.id = r.book_id  "\
                +"join members_profile p "\
                +"on p.id = r.user_id "\
                +"where r.date_time > NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7"

        cursor.execute(query)
        rows = dictfetchall(cursor)
        for row in rows:
            print(row)
            result.append(row)

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
