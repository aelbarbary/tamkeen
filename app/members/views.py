from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Event, Question, QuestionAnswer, Parent, Child
from django.urls import reverse
from django.conf import settings
import datetime
import logging
from django.db.models import Max, Sum, Count
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from .forms import ParentForm, ChildrenFormSet, EventForm


@csrf_exempt
def answerQuestion(request):
    name = request.POST.get('name')
    answer = request.POST.get('answer')
    id = request.POST.get('questionId')
    questionAnswer = QuestionAnswer (question_id = id, name = name, answer = answer, date_time = datetime.datetime.now() )
    questionAnswer.save()
    return HttpResponse()

def index(request):
    print (request.user)
    event_list = Event.objects.filter(date_time__gte=datetime.date.today()).order_by('date_time')[:5]
    question_list = Question.objects.exclude(closed=1).order_by('date_time').annotate(answers_count=Count('answers'))
    context = {'event_list': event_list,
                'question_list': question_list,
                'user_text': request.user if request.user.is_authenticated else 'login'}

    return render(request, 'index.html', context)

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


class ParentCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    model = Parent
    form_class = ParentForm
    success_url = 'thanks/'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        children_form = ChildrenFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  children_form=children_form,
                                  ))
    def post(self, request, *args, **kwargs):
        print(request)
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        children_form = ChildrenFormSet(self.request.POST)
        if (form.is_valid() and children_form.is_valid() and
            children_form.is_valid()):
            print("valid")
            return self.form_valid(form, children_form)
        else:
            print(children_form.errors)
            return self.form_invalid(form, children_form)

    def form_valid(self, form, children_form):
        self.object = form.save()
        children_form.instance = self.object
        children_form.save()
        children_form.instance = self.object
        children_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, children_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  children_form=children_form,
                                  ))

class EventRegisterView(CreateView):
    template_name = 'event/registration_form.html'
    model = Event
    fields = '__all__'
    success_url = 'thanks/'

    def get(self, request, event_id, *args, **kwargs):
        event = Event.objects.filter(id = event_id)[0]
        print(request.user.id)
        print(request.user.parent.id)
        children = Child.objects.filter(parent = request.user.parent.id).all()
        print(children)
        event_form = EventForm(instance=event)
        children_form = ChildrenFormSet(instance=request.user.parent)
        self.object = None
        return self.render_to_response(
            self.get_context_data(event_form=event_form,
                                  children_form = children_form
                                  ))
    def post(self, request, *args, **kwargs):
        print(request)
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        children_form = ChildrenFormSet(self.request.POST)
        if (form.is_valid() and children_form.is_valid() and
            children_form.is_valid()):
            print("valid")
            return self.form_valid(form, children_form)
        else:
            print(children_form.errors)
            return self.form_invalid(form, children_form)

    def form_valid(self, form, children_form):
        self.object = form.save()
        children_form.instance = self.object
        children_form.save()
        children_form.instance = self.object
        children_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, children_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  children_form=children_form,
                                  ))
