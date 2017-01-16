from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Youth
from django.urls import reverse

def index(request):
    youth_list = Youth.objects.order_by('age')[:100]
    context = {'youth_list': youth_list}
    return render(request, 'index.html', context)
