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
    url(r'^rest/attendancetrend/$', rest_attendance_trend, name='rest_attendance_trend'),
    url(r'^rest/attendancetrend/$', rest_attendance_trend, name='rest_attendance_trend'),
   ]
