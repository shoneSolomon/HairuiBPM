from django.template import Library as li
from django.shortcuts import render
from django.utils.safestring import mark_safe
from webserver.settings import APIURL
from gitc.models import Imgs, Video, Personnel, Article, Html,Library,Page

register = li()


@register.simple_tag
def makeimg(request, page_id, library_id, name):
    data_list = Imgs.objects.filter(ip_id=page_id, il_id=library_id)
    library_obj = Library.objects.filter(id=library_id).first()
    api = '%s/api/gitc/img/%s' % (APIURL,library_id)
    html = render(request, 'tmp/imgs.html', locals())
    return mark_safe(html.content)


@register.simple_tag
def makevideo(request, page_id, library_id, name):
    data_list = Video.objects.filter(vp_id=page_id, vl_id=library_id)
    library_obj = Library.objects.filter(id=library_id).first()
    api = '%s/api/gitc/video/%s' % (APIURL, library_id)
    html = render(request, 'tmp/video.html', locals())
    return mark_safe(html.content)


@register.simple_tag
def makearticle(request, page_id, library_id, name):
    data_list = Article.objects.filter(ap_id=page_id, al_id=library_id)
    library_obj = Library.objects.filter(id=library_id).first()
    api = '%s/api/gitc/article/%s' % (APIURL, library_id)
    html = render(request, 'tmp/article.html', locals())
    return mark_safe(html.content)


@register.simple_tag
def makepersonnel(request, page_id, library_id, name):
    data_list = Personnel.objects.filter(ppl_id=page_id, pl_id=library_id).order_by('ename')
    api = '%s/api/gitc/personnel/%s' % (APIURL, library_id)
    library_obj = Library.objects.filter(id=library_id).first()
    html = render(request, 'tmp/personnel.html', locals())
    return mark_safe(html.content)


@register.simple_tag
def makehtml(request, page_id, library_id, name):
    data_list = Html.objects.filter(hp_id=page_id, hl_id=library_id).count()
    if data_list:
        data_list = Html.objects.filter(hp_id=page_id, hl_id=library_id).first()
    library_obj = Library.objects.filter(id=library_id).first()
    api = '%s/api/gitc/html/%s' % (APIURL, library_id)
    html = render(request, 'tmp/html.html', locals())
    return mark_safe(html.content)

@register.simple_tag
def bt(meet):
    html = '<li><a><i class="fa fa-desktop"></i>%s<span class="fa fa-chevron-down"></span></a>'
    nub = Page.objects.filter(pp__domain=meet).count()
    html = html % meet.name if nub else ''
    return mark_safe(html)