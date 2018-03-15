from django.shortcuts import render
from members.models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.db import connection
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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
             and p.date_joined >= NOW() - interval '30 day'
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
             and p.date_joined >= NOW() - interval '14 day'
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
              and p.date_joined >= NOW() - interval '180 day'
            where a.date_time is null
        """

        cursor.execute(query)
        missing_for_6_month = cursor.fetchone()

        # Quiz answers
        query = """select a.text answer, q.text question, a.date_time
                from members_answer a
                join members_question q
                    on a.question_id = q.id
                where date_time > NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7"""

        cursor.execute(query)
        quiz_answers = dictfetchall(cursor)

        # New Members
        query = "select * " \
                +"from members_profile "\
                +"where date_joined > NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7"

        cursor.execute(query)
        new_members = dictfetchall(cursor)

        # Books checkouts
        query = "select * " \
                +"from members_bookreserve "\
                +"where date_time > NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7"

        cursor.execute(query)
        book_checkouts = dictfetchall(cursor)

        # Open your heart
        query = "select * " \
                +"from members_inquiry "\
                +"where date_time > NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7"

        cursor.execute(query)
        open_your_heart = dictfetchall(cursor)

    context = { 'total_users':total_users,
                'missing_for_a_month':missing_for_a_month[0],
                'missing_for_2_weeks': missing_for_2_weeks[0],
                'missing_for_6_month': missing_for_6_month[0],
                'total_males': total_males,
                'total_females' : total_females,
                'quiz_answers' : quiz_answers,
                'book_checkouts' : book_checkouts,
                'new_members' : new_members,
                'open_your_heart' : open_your_heart,
                }

    return render(request, 'dashboard_index.html', context)

@staff_member_required
def api_attendance_trend(request):
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
             and p.date_joined >= NOW() - interval '%s day'
            where a.date_time is null
            ORDER BY first_name, last_name
        """ % ( period_in_days, period_in_days)

        cursor.execute(query)
        users = dictfetchall(cursor)

        context = { 'users': users, 'absent_days': period_in_days }

    return render(request, 'people.html', context)

@csrf_exempt
@login_required
def quiz_history(request):
    with connection.cursor() as cursor:
        result = []
        query = """select
                quiz.id,
                quiz.name,
                quiz.date_time,
                (select count(1) from members_question where quiz_id = quiz.id) question_count  ,
                (select count(1) from members_question q join members_answer a on a.question_id = q.id where quiz_id = quiz.id) answer_count
                FROM members_quiz quiz
                ORDER BY date_time DESC"""

        cursor.execute(query)
        rows = dictfetchall(cursor)
        context = { 'results': rows  }

    return render(request, 'quiz_history.html', context)


def quiz_details(request, id):
    with connection.cursor() as cursor:
        result = []
        query = """
                select
                    quiz.name,
                    q.id question_id,
                    q.text question,
                    q.image question_image,
                    a.id answer_id,
                    a.date_time answer_date_time,
                    a.text answer,
                    a.score,
                    a.share_with_others,
                    p.first_name || ' ' || p.last_name user_name
                from members_quiz quiz
                join members_question q
                	on q.quiz_id = quiz.id
                left join members_answer a
                	on a.question_id = q.id
                left join members_profile p
                	on p.id = a.user_id
                where quiz_id = %s
                order by q.id, p.first_name
        """ % id

        cursor.execute(query, [date,date])
        rows = dictfetchall(cursor)
        context = { 'results': rows  }

    return render(request, 'quiz_details.html', context)

@csrf_exempt
@login_required
def user_profile(request, user_id):
    user = Profile.objects.get(pk = user_id)
    with connection.cursor() as cursor:
        result = []
        query = """select
                to_char(date_time, 'MM-DD-YYYY') date_time
                FROM members_attendance att
                WHERE user_id = %s
                ORDER BY att.date_time""" % user_id

        cursor.execute(query)
        attendance = dictfetchall(cursor)

        query = """select
                q.text question,
                a.text answer,
                to_char(a.date_time, 'MM-DD-YYYY') date_time
                FROM members_question q
                JOIN members_answer a
                    ON q.id = a.question_id
                WHERE user_id = %s
                ORDER BY date_time""" % user_id

        cursor.execute(query)
        answers = dictfetchall(cursor)

        context = {'user': user, 'attendance': attendance , 'answers': answers }

    return render(request, 'user_profile.html', context)
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
