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
from gitc.views import basics,logic

urlpatterns = [
    url(r'^index.html$', basics.indexview),
    url(r'^login.html$', basics.loginview),
    url(r'^logout.html$', basics.logoutview),
    url(r'^changepwd.html$', basics.changepwd),
    url(r'^domain/index.html$', logic.DomainView.as_view()),
    url(r'^library/index.html$', logic.LibraryView.as_view()),
    url(r'^page/index.html$', logic.PageView.as_view()),
    url(r'^template/index.html$', logic.TemplateView.as_view()),

    url(r'^contact.html$', basics.contact),
    url(r'^u/del/(?P<cid>\d+)$', basics.delcontact),

    url(r'^page/add.html$', logic.Addpage.as_view()),

    url(r'^page/(?P<cid>\d+)/index.html$', logic.UPageView.as_view()),

    url(r'^img-(?P<page_id>\d+)/(?P<library_id>\d+)/edit/(?P<cid>\d+)$', logic.ImgView.as_view()),
    url(r'^article-(?P<page_id>\d+)/(?P<library_id>\d+)/edit/(?P<cid>\d+)$', logic.ArticleView.as_view()),
    url(r'^personnel-(?P<page_id>\d+)/(?P<library_id>\d+)/edit/(?P<cid>\d+)$', logic.PersonnelView.as_view()),
    url(r'^personnel-(?P<page_id>\d+)/(?P<library_id>\d+)/import.html$', logic.ImportPerson.as_view()),
    url(r'^personnel/add/person$', logic.PersonAddAjax),
    url(r'^del/person/(?P<cid>\d+)$', logic.PersonDelAjax),

    url(r'^html-(?P<page_id>\d+)/(?P<library_id>\d+)/edit/(?P<cid>\d+)$', logic.HtmlView.as_view()),

    url(r'^kindeditor/upload.html$', logic.upload_kindeditor_img),
    # url(r'', basics.indexview),

]
