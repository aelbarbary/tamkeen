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
    url(r'^api/video/play/$', main_view.play_video, name='play_video'),
    #quiz
    url(r'^quiz/$', quiz_view.quiz, name='quiz'),

    # Attendance
    url(r'^attendance/$', attendance_view.attendance_sheet, name='attendance_sheet'),

    url(r'^api/attendance/checkin$', attendance_view.api_checkin, name='api_checkin'),
    url(r'^api/attendance/checkout$', attendance_view.api_checkout, name='api_checkout'),
    url(r'^api/attendance/(?P<date>\d+)/$', attendance_view.api_attendance_sheet, name='api_attendance_sheet'),

    # Books
    url(r'^books/$', books_view.show_books, name='show_books'),
    url(r'^api/books/$', books_view.get_books, name='get_books'),
    url(r'^api/books/requested$', books_view.get_requested_books, name='get_requested_books'),
    url(r'^api/books/(?P<id>\d+)/reserve/$', books_view.reserve_book, name='reserve_book'),

    # Accounts management Endpoints
    url(r'^accounts/register/thanks/', user_view.registration_thanks, name='registration_thanks'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^profile/$', user_view.profile, name='profile'),
    url(r'^password/change/$', user_view.change_password, name='change_password'),
    url(r'^register/$', user_view.NewMemberRequest.as_view(), name='new_member_request'),
    url(r'^api/members/$', user_view.members, name='members'),
    url(r'^members/$', user_view.show_members, name='show_members'),
]
