from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from django.urls import reverse
from django.conf import settings
import datetime
import logging
from django.db.models import Max, Sum, Count
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from .forms import AnswerForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import threading
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.db.models import Q

def index(request):
    print (request.user)
    # question_list = Question.objects.exclude(closed=1).order_by('date_time').annotate(answers_count=Count('answers'))
    context = { 'user_text': request.user if request.user.is_authenticated else 'login'}

    return render(request, 'index.html', context)

@csrf_exempt
@login_required
def quiz(request):
    user_id = request.user.id

    if request.method == 'POST':


        print(user_id)
        answers = request.POST.get('answer-11')
        quiz_id = request.POST.get('quiz-id')

        quiz = Quiz.objects.get(pk=quiz_id)
        questions = quiz.questions.all()
        for q in questions:
            answer_text =  request.POST.get('answer-' + str(q.id))
            answer = Answer(text=answer_text, date_time = datetime.datetime.now(), score = 0, question_id = q.id, user_id = user_id )
            answer.save()

        return render(request, 'quiz-thanks.html')
    else:

        print (request.user)
        quizs = Quiz.objects.order_by('-id')[:1]
        print("quizs %s" % quizs)
        if quizs:
            last_quiz = quizs[0]
            questions = last_quiz.questions.all().order_by("id")

            answers = Answer.objects.filter(question_id__in=questions).filter(user_id = user_id )
            if answers:
                    print(answers)
                    return render(request, 'quiz-thanks.html')
            else:
                context = {'quiz': last_quiz, 'questions': questions }
                return render(request, 'quiz.html', context)

def thanks(request):
    return render(request, 'thanks.html', {})

def registration_activate(request, key):
    return render(request, 'thanks.html', {})

def questionsHistory(request):
    questions = Question.objects.exclude(closed=0).order_by('date_time')
    score =0
    for q in questions:
        answer = QuestionAnswer.objects.filter(question = q.id).order_by('-score', 'date_time')[:1]
        q.answer = answer[0].answer
        q.name = answer[0].name
        q.totalPoints = QuestionAnswer.objects.filter(name = q.name).aggregate(Sum('score'))["score__sum"]
        score = answer[0].score

        rank =  getRank(score)
        q.rankImage = rank["rankImage"]
        q.rank = rank["rank"]

    personList = QuestionAnswer.objects.values('name').annotate(score = Sum('score')).order_by('-score')
    for person in personList:
        rank =  getRank(person["score"])
        person["rankImage"] = rank["rankImage"]

    context = {'questions': questions,
                'personList': personList,
                'scoreRange': range(score)}
    return render(request, 'questions-history.html', context)

@staff_member_required
def members(request):
    members = Profile.objects.order_by('first_name', 'last_name')
    data = json.dumps([member.json for member in members])
    return HttpResponse(data, content_type='application/json')

@staff_member_required
def show_members(request):
    return render(request, 'view-members.html')


def books(request):
    user = request.user.id
    print(user)
    books = Book.objects.exclude(book_reserves__user_id=user).order_by('name', 'status')
    data = json.dumps([book.json for book in books])
    return HttpResponse(data, content_type='application/json')

@login_required
def show_books(request):
    return render(request, 'view-books.html')

@csrf_exempt
def reserve_book(request, id):
    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        user_id = json_data["userId"]
        book_id = id
        request = BookReserve(user_id=user_id, book_id = book_id, date_time = datetime.datetime.now() )
        request.save()
        return HttpResponse("done")
    else:
        return HttpResponse()
