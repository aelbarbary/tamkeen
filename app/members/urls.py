from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from . import views
from registration.backends.hmac.views import RegistrationView
# from .views import AnswerView
from django.contrib.auth.decorators import login_required

app_name = 'members'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^quiz/$', views.quiz, name='quiz'),
    # url(r'^questionsHistory/', views.questionsHistory, name='questionsHistory'),
    # url(r'^question/(?P<question_id>[0-9]+)/$', login_required(AnswerQuestionView.as_view()), name='question'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/register/thanks/', views.thanks, name='thanks')
]
