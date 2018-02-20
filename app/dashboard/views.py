from django.shortcuts import render
from members.models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.db import connection

@staff_member_required
def index(request):
    total_users = Profile.objects.all().count()
    with connection.cursor() as cursor:
        # USer Info completeness
        query = """
                select count(1) as total_count, to_char( date(date_time), 'YYYY-MM-DD')
                from members_attendance
                group by to_char(date(date_time), 'YYYY-MM-DD')
                order by to_char(date(date_time), 'YYYY-MM-DD')
        """
        cursor.execute(query)
        # attendance = cursor.fetchall()
        attendance = dictfetchall(cursor)

    context = { 'total_users':total_users, 'attendance': str(attendance)}


    return render(request, 'dashboard_index.html', context)

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
