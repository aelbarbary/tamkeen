from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Youth, Event, EventImages, Question, QuestionAnswer
from django.urls import reverse
from django.conf import settings
import datetime
from .forms import NewMemberForm
import logging
from django.db.models import Max, Sum, Count
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def answerQuestion(request):
    print("answring questions")
    name = request.POST.get('name')
    answer = request.POST.get('answer')
    id = request.POST.get('questionId')
    questionAnswer = QuestionAnswer (question_id = id, name = name, answer = answer, date_time = datetime.datetime.now() )
    questionAnswer.save()
    return HttpResponse()

def index(request):
    event_list = Event.objects.filter(date_time__gte=datetime.date.today()).order_by('date_time')[:5]
    gallery_list = Event.objects.filter(date_time__lt=datetime.date.today()).order_by('date_time')[:5]
    for gal in gallery_list:
        event_image = EventImages.objects.filter(event = gal.id)
        gal.image = gal.flyer if len(event_image) == 0 else event_image[0].image
        event_date = gal.date_time.replace(tzinfo=None)
        gal.since = (datetime.datetime.utcnow() - event_date).days

    question_list = Question.objects.exclude(closed=1).order_by('date_time').annotate(answers_count=Count('answers'))

    context = {'event_list': event_list,
                'gallery_list': gallery_list,
                'question_list': question_list}

    return render(request, 'index.html', context)

def join(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewMemberForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thanks/')
    else:
        form = NewMemberForm()

    return render(request, 'join.html', {'form': form})

def thanks(request):
    return render(request, 'thanks.html', {})

def questionsHistory(request):
    questions = Question.objects.exclude(closed=0).order_by('date_time')
    score =0
    for q in questions:
        answer = QuestionAnswer.objects.filter(question = q.id).order_by('-score')[:1]
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
                'personList': personList}
    return render(request, 'questions-history.html', context)

def getRank(score):
    if score >= 320:
        return
        {   'rankImage': "images/ranks/king.png",
            'rank': "King. you are the man!" }
    elif score >= 160:
        return { 'rankImage': "images/ranks/prime-minister.png",
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
