from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from . import views
from registration.backends.hmac.views import RegistrationView
from .views import ParentCreateView, EventRegisterView, AnswerQuestionView
from django.contrib.auth.decorators import login_required

app_name = 'members'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^questionsHistory/', views.questionsHistory, name='questionsHistory'),
    url(r'^question/(?P<question_id>[0-9]+)/$', login_required(AnswerQuestionView.as_view()), name='question'),
    # url(r'^answerQuestion/', views.answerQuestion, name='answerQuestion'),
    url(r'^accounts/register/$',
        ParentCreateView.as_view(),
        name='registration_register',
    ),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/register/thanks/', views.thanks, name='thanks'),
    url(r'^events/(?P<event_id>[0-9]+)/register/$',
        EventRegisterView.as_view(),
        name='event_register',
        ),

    url(r'^whatsapp/subscribe/$', views.whatsapp_subscribe,name='whatsapp_subscribe')
]
