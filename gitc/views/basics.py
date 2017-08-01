from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from gitc.models import *
from gitc.gform import *
from gitc.pages import Pagination
import json


def loginview(request):
    title = 'GITC后台管理'
    if request.method == 'GET':
        return render(request, 'login.html', locals())
    elif request.method == 'POST':
        username = request.POST.get('username')
        pasw = request.POST.get('password')
        user = authenticate(username=username, password=pasw)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/gitcadmin/index.html'))
        error = '账号或密码错误！'
        return render(request, 'login.html', locals())


def logoutview(request):
    logout(request)
    return redirect('/gitcadmin/login.html')


@login_required
def changepwd(request):
    if request.method == 'GET':
        obj = ChangepwdForm()
        return render(request, 'changepwd.html', locals())
    else:
        obj = ChangepwdForm(request.POST)
        if obj.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
                return redirect('/gitcadmin/index.html')
            else:
                oldpassword_is_wrong = True
                errmsg = '原密码不正确！请重新输入！'
                return render(request, 'changepwd.html', locals())
        else:
            oldpassword_is_wrong = True
            errmsg = '2次输入密码不正确！'
            return render(request, 'changepwd.html', locals())


@login_required
def indexview(request):
    page = Page.objects.all().count()
    jiabin = Personnel.objects.all().count()
    yhs = Contact.objects.all().count()
    tp = Imgs.objects.all().count()
    domain_list = Domain.objects.all()
    return render(request, 'index.html', locals())


@login_required
def contact(request):
    p = request.GET.get('p', 1)
    url = '/gitcadmin/contact.html'
    pagemax_nub = 10  # 每页显示几条数据
    maxPageNu = 7  # 最大显示几页
    data = Contact.objects.all().order_by('-creat_at')
    page_obj = Pagination(data.count(), p, url, pagemax_nub, maxPageNu)
    data = data[page_obj.start:page_obj.end]
    domain_list = Domain.objects.all()
    return render(request, 'admin/contactlist.html', locals())


@login_required
def delcontact(request, cid):
    ret = Contact.objects.filter(id=cid).delete()
    if ret:
        return HttpResponse(json.dumps({'status': True}))
    return HttpResponse(json.dumps({'status': False}))


