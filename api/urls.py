"""webserver URL Configuration

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
from django.conf.urls import url
from django.shortcuts import HttpResponse
from . import views

def error(request):
    return HttpResponse('404')

urlpatterns = [
    url(r'^gitc/pic/(?P<pictype>\d+)$', views.getpic),
    url(r'^gitc/user/(?P<meet_id>\d+)$', views.getperson),
    url(r'^gitc/meet/(?P<meet_id>\d+)$', views.getmeet),
    url(r'^gitc/imguplod/uplod.html$', views.imgup),
    url(r'',error ),
]
