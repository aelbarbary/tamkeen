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

@csrf_exempt
@login_required
def quiz_history(request):
    with connection.cursor() as cursor:
        result = []
        query = """select
                quiz.id,
                quiz.name,
                (select count(1) from members_question where quiz_id = quiz.id) question_count  ,
                (select count(1) from members_question q join members_answer a on a.question_id = q.id where quiz_id = quiz.id) answer_count
                from members_quiz quiz
                order by id desc"""

        cursor.execute(query, [date,date])
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
