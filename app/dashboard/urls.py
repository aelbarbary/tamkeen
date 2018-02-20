from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from dashboard.views import *

app_name = 'dashboard'
urlpatterns = [
    url(r'^$', index, name='index'),
   ]
