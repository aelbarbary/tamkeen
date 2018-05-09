from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'dashboard'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^people/$', people, name='people'),
    url(r'^calendar/$', calendar, name='calendar'),
    url(r'^people/absent/(?P<period_in_days>\d+)/$', absent, name='absent'),
    url(r'^people/(?P<user_id>\d+)/$', user_profile, name='user_profile'),
    url(r'^api/attendancetrend/$', api_attendance_trend, name='api_attendance_trend'),
    url(r'^api/attendancetrend/$', api_attendance_trend, name='api_attendance_trend'),
    url(r'^api/carpool/drive$', api_carpool_drive, name='api_carpool_drive'),
    url(r'^quiz/history$', quiz_history, name='quiz_history'),
    url(r'^quiz/(?P<id>\d+)/$', quiz_details, name='quiz_details'),
    url(r'^quiz/emailview/$', quiz_email_view, name='quiz_email_view'),
    url(r'^carpool/$', carpool, name='carpool'),
   ]
