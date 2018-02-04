from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from members.models import *
from django.urls import reverse
from django.conf import settings
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
import random
import string


@login_required
def profile(request):
    profile = Profile.objects.get(pk=request.user.id)
    if profile.skills:
        skills = profile.skills.split(",")
    else:
        skills = []
    answers_count = Answer.objects.filter(user_id=request.user.id).count()
    awards_count = UserAward.objects.filter(user_id=request.user.id).count()
    context = { 'user': profile, 'skills': skills, 'answers_count': answers_count, 'awards_count': awards_count }
    return render(request, 'profile.html', context )

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {
        'form': form
    })

class NewMemberRequest(CreateView):
    success_url = '/accounts/register/thanks/'
    template_name = 'newmemberrequest_form.html'
    model = NewMemberRequest
    form_class = NewMemberRequestForm
    def form_valid(self, form):
        response = super(NewMemberRequest, self).form_valid(form)
        instance = self.object
        user_name = '%s.%s' % (instance.first_name.replace(" ", "").lower(), instance.last_name.replace(" ", "").lower())
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        new_user = Profile.objects.create_user(user_name,
                                        instance.email,
                                        password,
                                        first_name = instance.first_name,
                                        last_name = instance.last_name,
                                        gender = instance.gender,
                                        dob=datetime.now())
        new_user.save()

        subject = 'Your account was created successfully!'
        recepients = [instance.email]

        message = "%s, Thank you for registering. your user information is listed below. \n" % (instance.first_name)
        message = "User Name: %s \n" % (user_name)
        message += "Password: %s\n" % password

        EmailSender(instance, subject, message, recepients).start()

        return response

def registration_thanks(request):
    return render(request, 'thanks.html', {})

def registration_activate(request, key):
    return render(request, 'thanks.html', {})

@staff_member_required
def members(request):
    members = Profile.objects.order_by('first_name', 'last_name')
    data = json.dumps([member.json for member in members])
    return HttpResponse(data, content_type='application/json')

@staff_member_required
def show_members(request):
    return render(request, 'view-members.html')
