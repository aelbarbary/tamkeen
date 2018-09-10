"""tamkeen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import  (login,
                                    logout,
                                    password_reset,
                                    password_reset_done,
                                    password_reset_confirm,
                                )
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'', include('members.urls')),
    url(r'dashboard/', include('dashboard.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^password_reset/$', auth_views.password_reset,{'email_template_name':'registration/password_reset_email.txt',
                                                    'subject_template_name':'registration/password_reset_subject.txt',
                                                    'post_reset_redirect':'password_reset_done',
                                                    'from_email':'abdelrahman.elbarbary@gmail.com',
                                                    },name='password_reset'),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'template_name': 'registration/password_reset_confirm.txt'}, name='password_reset_confirm'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'registration/password_reset_done.txt'}, name='password_reset_done'),
    url(r'^password_reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
