from django.shortcuts import render
from members.models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.db import connection
import json
from django.http import HttpResponseRedirect, HttpResponse

@staff_member_required
def index(request):
    total_users = Profile.objects.all().count()
    total_males = Profile.objects.all().filter(gender='M').count()
    total_females = Profile.objects.all().filter(gender='F').count()

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

    context = { 'total_users':total_users,
                'missing_for_a_month':missing_for_a_month[0],
                'missing_for_2_weeks': missing_for_2_weeks[0],
                'missing_for_6_month': missing_for_6_month[0],
                'total_males': total_males,
                'total_females' : total_females}

    return render(request, 'dashboard_index.html', context)

@staff_member_required
def rest_attendance_trend(request):
    result = []
    with connection.cursor() as cursor:
        query = """
                select count(1) as total_count, to_char( date(date_time) , 'YYYY-MM-DD') as date
                from members_attendance
                group by to_char(date(date_time), 'YYYY-MM-DD')
                order by to_char(date(date_time), 'YYYY-MM-DD')
        """

        cursor.execute(query)
        attendance = dictfetchall(cursor)

    context = { 'attendance': attendance}

    data = json.dumps(context)

    return HttpResponse(data, content_type='application/json')

@staff_member_required
def people(request):
    users = Profile.objects.all().order_by('first_name', 'last_name')
    context = { 'users':users}
    return render(request, 'people.html', context)

staff_member_required
def calendar(request):
    context = { }
    return render(request, 'calendar.html', context)

@staff_member_required
def absent(request, period_in_days):
    context = {}
    with connection.cursor() as cursor:

        query = """
            select p.id, p.first_name, p.last_name, p.dob, p.gender
            from members_profile p
            left  join members_attendance a
             on a.user_id = p.id
             and a.date_time >= NOW() - interval '%s day'
            where a.date_time is null
            ORDER BY first_name, last_name
        """ % period_in_days

        cursor.execute(query)
        users = dictfetchall(cursor)

        context = { 'users': users, 'absent_days': period_in_days }

    return render(request, 'people.html', context)


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
