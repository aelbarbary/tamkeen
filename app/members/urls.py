from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from .  import forms
from members.views import *

app_name = 'members'
urlpatterns = [

    #main
    url(r'^$', main_view.index, name='index'),
    url(r'^openyourheart/$', main_view.InquiryCreate.as_view(), name='new_inquiry'),
    url(r'^videos/$', main_view.get_videos, name='view_videos'),
    url(r'^rest/video/play/$', main_view.play_video, name='play_video'),
    url(r'^stats/$', main_view.stats, name='stats'),

    #quiz
    url(r'^quiz/$', quiz_view.quiz, name='quiz'),

    # Attendance
    url(r'^attendance/$', attendance_view.attendance_sheet, name='attendance_sheet'),
    url(r'^rest/members/attendance/checkin$', attendance_view.rest_checkin, name='rest_checkin'),
    url(r'^rest/members/attendance/checkout$', attendance_view.rest_checkout, name='rest_checkout'),
    url(r'^rest/members/attendance/(?P<date>\d+)/$', attendance_view.rest_attendance_sheet, name='rest_attendance_sheet'),

    # Books
    url(r'^books/$', books_view.show_books, name='show_books'),
    url(r'^rest/books/$', books_view.get_books, name='get_books'),
    url(r'^rest/books/requested$', books_view.get_requested_books, name='get_requested_books'),
    url(r'^rest/books/(?P<id>\d+)/reserve/$', books_view.reserve_book, name='reserve_book'),

    # Accounts management Endpoints
    url(r'^accounts/register/thanks/', user_view.registration_thanks, name='registration_thanks'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^profile/$', user_view.profile, name='profile'),
    url(r'^password/change/$', user_view.change_password, name='change_password'),
    url(r'^register/$', user_view.NewMemberRequest.as_view(), name='new_member_request'),
    url(r'^rest/members/$', user_view.members, name='members'),
    url(r'^members/$', user_view.show_members, name='show_members'),
]
