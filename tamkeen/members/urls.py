from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'members'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^event/', views.event, name='event'),
    url(r'^allevents/', views.all_events, name='all_events'),
    url(r'^member/', views.all_members, name='all_members'),
]
