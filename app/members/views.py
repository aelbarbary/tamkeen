from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Youth, Event
from django.urls import reverse
from django.conf import settings
import datetime
from .forms import NewMemberForm

def index(request):
    event_list = Event.objects.filter(date_time__gte=datetime.date.today()).order_by('date_time')[:5]
    context = {'event_list': event_list}
    return render(request, 'index.html', context)

def new_member(request):
    if request.method == 'POST':
        print(request.FILES)
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
