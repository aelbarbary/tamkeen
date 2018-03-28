from django.shortcuts import render
from members.models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.db import connection
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
import boto3
from django.conf import settings

@staff_member_required
def index(request):
    total_users = Profile.objects.all().count()
    total_males = Profile.objects.all().filter(gender='M').count()
    total_females = Profile.objects.all().filter(gender='F').count()
    base_query = """
        select count(1) from members_profile p
        left  join members_attendance a
         on a.user_id = p.id
         and a.date_time >= NOW() - interval '%(period)d day'
        where a.date_time is null
        and p.date_joined <= NOW() - interval '%(period)d day'
    """
    with connection.cursor() as cursor:
        # missing for 2 weeks answers
        params = { 'period' : 14 }
        query = base_query % params
        cursor.execute(query)
        missing_for_2_weeks = cursor.fetchone()

        # missing for a month
        params = { 'period' : 30 }
        query = base_query % params
        cursor.execute(query)
        missing_for_a_month = cursor.fetchone()

        # missing for 6 month
        params = { 'period' : 180 }
        query = base_query % params
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
            where a.date_time is null
            and p.date_joined <= NOW() - interval '%s day'
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

@csrf_exempt
@login_required
def carpool(request):
    today = datetime.now().strftime('%Y%m%d')
    print(today)
    with connection.cursor() as cursor:
        result = []
        query = """select
                distinct p.id,
                        p.first_name || ' ' || p.last_name as passenger_name,
                        driver.first_name || ' ' || driver.last_name driver_name
                FROM members_attendance att
                JOIN members_profile p
                    on p.id = att.user_id
                LEFT JOIN members_carpool cp
                    on p.id = cp.passenger_id
                    and cp.date_time>= date_trunc('day', to_date(%s, 'YYYYMMDD'))
                    and cp.date_time < date_trunc('day', to_date(%s, 'YYYYMMDD') + 1)
                LEFT JOIN members_profile driver
                    on cp.driver_id = driver.id
                WHERE  att.date_time >= date_trunc('day', to_date(%s, 'YYYYMMDD'))
                and att.date_time < date_trunc('day', to_date(%s, 'YYYYMMDD') + 1)
                order by p.first_name || ' ' || p.last_name

                """


        cursor.execute(query, [today, today, today, today])
        passengers = dictfetchall(cursor)
        print(passengers)
        context = {'passengers': passengers}

    return render(request, 'carpool.html', context)

@csrf_exempt
@login_required
def api_carpool_checkin(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        passenger_id = json_data["passengerId"]
        driver_id = request.user.id;
        print(driver_id)
        date = datetime.now().date()
        print(date)
        # date = datetime.strptime(date,'%Y%m%d %H:%M:%S')
        driver = Profile.objects.get(pk=driver_id)
        print(driver)
        carpool = Carpool(driver_id=driver_id, passenger_id = passenger_id, date_time = date )
        carpool.save()

        context = { 'driver': "%s %s" % (driver.first_name, driver.last_name) }

        data = json.dumps(context)

        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponse()

@csrf_exempt
@login_required
def api_carpool_drive(request):

    if request.method == "POST":
        driver_id = request.user.id;
        # get passengers
        with connection.cursor() as cursor:
            result = []
            query = """select distinct p.first_name || ' ' || p.last_name as name
                FROM members_profile p
                JOIN members_carpool cp
                    on p.id = cp.passenger_id
                WHERE cp.date_time>= date_trunc('day', current_date)
                and cp.date_time < date_trunc('day', current_date + 1)
                and cp.driver_id = %s
                order by p.first_name || ' ' || p.last_name
                """ % driver_id

            cursor.execute(query)
            passengers = cursor.fetchall()
            p_list = []
            for p in passengers:
                # words.append(row['unites_lexicales'])
                p_list.append(p[0])

            passengers_list = ", ".join(p_list)
            print(passengers_list)

        #get driver
        driver = Profile.objects.get(pk=driver_id)

        #get remaining kids
        with connection.cursor() as cursor:
            result = []
            query = """select count(1)
                FROM members_attendance att
                JOIN members_profile p
                    on p.id = att.user_id
                LEFT JOIN members_carpool cp
                    on p.id = cp.passenger_id
                    and cp.date_time>= date_trunc('day', current_date)
                    and cp.date_time < date_trunc('day', current_date + 1)
                WHERE  att.date_time >= date_trunc('day', current_date)
                and att.date_time < date_trunc('day', current_date + 1)
                and p.is_staff = false
                and cp.id IS NULL
                """

            cursor.execute(query)
            result = cursor.fetchone()
            left_out_kids = result[0]

        driver_name = driver.first_name + ' ' + driver.last_name
        # send message to carpool ADMINS
        send_sms_to_admins(driver_name, passengers_list, left_out_kids)

        return HttpResponse('Ok')
    else:
        return HttpResponse()

def send_sms_to_admins(driver_name, passengers_list, left_out_kids):
    # Create an SNS client
    client = boto3.client(
        "sns",
        aws_access_key_id= settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name="us-west-2"
    )

    # Create the topic if it doesn't exist (this is idempotent)
    topic = client.create_topic(Name="notifications")
    topic_arn = topic['TopicArn']  # get its Amazon Resource Name

    # Add SMS Subscribers
    for number in settings.CARPOOL_ADMINS:
        client.subscribe(
            TopicArn=topic_arn,
            Protocol='sms',
            Endpoint=number  # <-- number who'll receive an SMS message.
        )

    # Publish a message.
    client.publish(Message="Driver %s has just picked up %s ... there are %s kids are left out!"
                    % ( driver_name, passengers_list, left_out_kids )
                    , TopicArn=topic_arn)

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
