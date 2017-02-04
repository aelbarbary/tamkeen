from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'members'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^join/', views.new_member, name='join'),
    url(r'^thanks/', views.thanks, name='thanks'),
    url(r'^(?P<event_id>[0-9]+)/gallery/$', views.gallery, name='gallery'),
]
