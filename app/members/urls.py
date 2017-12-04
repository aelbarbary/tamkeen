from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from . import views
from registration.backends.simple.views import RegistrationView
# from .views import AnswerView
from django.contrib.auth.decorators import login_required
from .  import forms

app_name = 'members'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^quiz/$', views.quiz, name='quiz'),
    url(r'^members/$', views.show_members, name='show_members'),
    url(r'^attendance/$', views.attendance_sheet, name='attendance_sheet'),
    url(r'^books/$', views.show_books, name='show_books'),
    url(r'^openyourheart/$', views.InquiryCreate.as_view(), name='new_inquiry'),
    url(r'^videos/$', views.get_videos, name='view_videos'),
    url(r'^stats/$', views.stats, name='stats'),

    # Account management Endpoints
    url(r'^accounts/register/thanks/', views.thanks, name='thanks'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^password/change/$', views.change_password, name='change_password'),
    url(r'^register/$', views.NewMemberRequest.as_view(), name='new_member_request'),

    # Rest End points
    url(r'^rest/members/attendance/new$', views.record_attendacne, name='record_attendacne'),
    url(r'^rest/members/attendance/(?P<date>\d+)/$', views.rest_attendance_sheet, name='rest_attendance_sheet'),
    url(r'^rest/books/$', views.get_books, name='get_books'),
    url(r'^rest/books/requested$', views.get_requested_books, name='get_requested_books'),
    url(r'^rest/members/$', views.members, name='members'),
    url(r'^rest/books/(?P<id>\d+)/reserve/$', views.reserve_book, name='reserve_book'),
]
