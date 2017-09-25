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

# @csrf_exempt
# def answerQuestion(request):
#     name = request.POST.get('name')
#     answer = request.POST.get('answer')
#     id = request.POST.get('questionId')
#     questionAnswer = QuestionAnswer (question_id = id, name = name, answer = answer, date_time = datetime.datetime.now() )
#     questionAnswer.save()
#     return HttpResponse()


# class AnswerQuestionView(CreateView):
#     template_name = 'answer-question.html'
#     model = QuestionAnswer
#     fields = '__all__'
#     success_url = '/'
#
#     def get(self, request, question_id, *args, **kwargs):
#         question = Question.objects.filter(id = question_id)[0]
#         print(request.user.id)
#         print(self)
#         answer_question_form = AnswerQuestionForm(instance=question)
#         self.object = None
#         return self.render_to_response(
#             self.get_context_data( question = question,
#                                    answer_question_form=answer_question_form
#                                   ))
#     def post(self, request, question_id, *args, **kwargs):
#         print(request)
#         self.object = None
#         form = AnswerQuestionForm(request.POST)
#         if form.is_valid():
#             answer = form.save(commit=False)
#             answer.question_id = question_id
#             answer.user_id = request.user.id
#             answer.save()
#             print("valid")
#             return self.form_valid(form)
#         else:
#             print("invalid")
#             print(form.errors)
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponseRedirect(self.get_success_url())
#
#     def form_invalid(self, form, ):
#         return self.render_to_response(
#                 self.get_context_data(form=form))

def index(request):
    print (request.user)
    # question_list = Question.objects.exclude(closed=1).order_by('date_time').annotate(answers_count=Count('answers'))
    context = { 'user_text': request.user if request.user.is_authenticated else 'login'}

    return render(request, 'index.html', context)

@csrf_exempt
@login_required
def quiz(request):
    if request.method == 'POST':

        user_id = request.user.id
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
            questions = last_quiz.questions.all()

            answers = Answer.objects.filter(question_id__in=questions)
            if answers:
                    print(answers)
                    return render(request, 'quiz-thanks.html')
            else:
                context = {'quiz': last_quiz, 'questions': questions }
                return render(request, 'quiz.html', context)

def thanks(request):
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

def getRank(score):
    if score >= 320:
        return
        {   'rankImage': "images/ranks/king.png",
            'rank': "King. you are the man!" }
    elif score >= 160:
        return { 'rankImage': "images/ranks/second-in-command.png",
                'rank': "Prime Minister. Get 320 points to be the King!"}
    elif score >= 80:
        return {'rankImage' : "images/ranks/rock.png",
                'rank' : "Rock. Get 160 points to be a Prime Minister"}
    elif score >= 40:
        return { 'rankImage': "images/ranks/bishop.png",
                 'rank': "Bishop. you need to get to 80 points to be a Rock"}
    elif score >=20:
        return { 'rankImage': "images/ranks/knight.png",
                'rank':  "Knight. You need to have 40 points to be a Bishop"}
    else:
        return { 'rankImage': "images/ranks/pawn.png",
                'rank': "Pawn. get 20 points to be a Knight" }
