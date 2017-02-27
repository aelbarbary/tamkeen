from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Youth, Event, EventImages, Question, QuestionAnswer
from django.urls import reverse
from django.conf import settings
import datetime
from .forms import NewMemberForm
import logging
from django.db.models import Max, Sum


def index(request):
    if request.method == 'POST':
        name = request.POST['name']
        answer = request.POST['answer']
        id = request.POST['question-id']
        print(name )
        print(answer )
        questionAnswer = QuestionAnswer (question_id = id, name = name, answer = answer, date_time = datetime.date.today() )
        questionAnswer.save()
        return HttpResponseRedirect('/thanks/')

    else:
        print("not post")
        event_list = Event.objects.filter(date_time__gte=datetime.date.today()).order_by('date_time')[:5]
        gallery_list = Event.objects.filter(date_time__lt=datetime.date.today()).order_by('date_time')[:5]
        for gal in gallery_list:
            event_image = EventImages.objects.filter(event = gal.id)
            gal.image = gal.flyer if len(event_image) == 0 else event_image[0].image
            event_date = gal.date_time.replace(tzinfo=None)
            gal.since = (datetime.datetime.utcnow() - event_date).days

        question = Question.objects.exclude(closed=1).order_by('date_time')[:1]

        context = {'event_list': event_list,
                    'gallery_list': gallery_list,
                    'question': question}
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

# def gallery(request, event_id):
#     event_images = EventImages.objects.filter(event = event_id)
#     context = {'event_images': event_images}
#     return render(request, 'gallery.html', context)

def questionsHistory(request):
    questions = Question.objects.exclude(closed=0).order_by('date_time')
    print(questions.count())
    score =0
    for q in questions:
        answer = QuestionAnswer.objects.filter(question = q.id).order_by('-score')[:1]
        q.answer = answer[0].answer
        q.name = answer[0].name
        q.totalPoints = QuestionAnswer.objects.filter(name = q.name).aggregate(Sum('score'))["score__sum"]
        score = answer[0].score

    context = {'questions': questions , 'scoreRange': range(score)  }
    return render(request, 'questions-history.html', context)
