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
            print(request.POST.get('share-with-others-' + str(q.id)))
            share_with_others = request.POST.get('share-with-others-' + str(q.id)) == 'on'
            print("share_with_others : %s" % share_with_others)
            answer = Answer(text=answer_text,
                            date_time = datetime.now(),
                            score = 0,
                            question_id = q.id,
                            user_id = user_id,
                            share_with_others = share_with_others )
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
