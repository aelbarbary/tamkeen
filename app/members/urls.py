from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .forms import RegisterForm
from registration.backends.hmac.views import RegistrationView

app_name = 'members'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^thanks/', views.thanks, name='thanks'),
    url(r'^questionsHistory/', views.questionsHistory, name='questionsHistory'),
    url(r'^answerQuestion/', views.answerQuestion, name='answerQuestion'),
    url(r'^accounts/register/$',
        RegistrationView.as_view(
            form_class=RegisterForm
        ),
        name='registration_register',
    ),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # url(r'^(?P<event_id>[0-9]+)/gallery/$', views.gallery, name='gallery'),
]
