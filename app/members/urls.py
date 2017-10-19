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
    url(r'^rest/members/$', views.members, name='members'),
    url(r'^members/$', views.show_members, name='show_members'),
    url(r'^accounts/register/$',
        RegistrationView.as_view(
            form_class=forms.CustomUserCreationForm
        ),
        name='registration_register',
    ),
    url(r'^accounts/register/thanks/', views.thanks, name='thanks'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^rest/books/(?P<id>\d+)/reserve/$', views.reserve_book, name='reserve_book'),
    url(r'^rest/books/$', views.books, name='books'),
    url(r'^books/', views.show_books, name='show_books'),


]
