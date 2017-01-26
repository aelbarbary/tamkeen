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
        # create a form instance and populate it with data from the request:
        form = NewMemberForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_youth = form.save()
            print(new_youth)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewMemberForm()

    return render(request, 'join.html', {'form': form})
