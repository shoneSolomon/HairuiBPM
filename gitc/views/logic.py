from django.shortcuts import render, redirect, HttpResponse
from gitc.views.baseview import BaseView
from gitc.views.utils import md5
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from gitc.models import *
from gitc.gform import *
import json


class Addpage(BaseView):
    '''添加页面'''

    def get(self, request):
        domain_list = Domain.objects.all()
        return render(request, 'admin/addpage.html', locals())

    def post(self, request):
        '''
        ajax请求,创建页面
        :param request:
        :return:
        '''
        data = {'status': True, 'url': '', 'msg': None}
        obj = PageForm(request.POST)
        if obj.is_valid():
            p_obj = Page.objects.create(**obj.cleaned_data)
            if p_obj:
                data['url'] = '/gitcadmin/page/%s/index.html' % p_obj.id
            else:
                data['status'] = False
                data['msg'] = '没有创建成功！'
        else:
            data['status'] = False
            data['msg'] = '验证未通过！'
        return HttpResponse(json.dumps(data))


class PageView(BaseView):
    def get(self, request, cid):
        domain_list = Domain.objects.all()
        obj = Page.objects.filter(id=cid).first()
        library_list = obj.pp.library_set.all()
        return render(request, 'admin/pagelist.html', locals())


class ImgView(BaseView):

    def get(self, request, page_id, library_id, cid):
        domain_list = Domain.objects.all()
        info = {'ip_id': page_id, 'il_id': library_id}
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        if int(cid) == 0:
            title = '添加图片'
        else:
            if Imgs.objects.filter(id=cid).count():
                img_obj = Imgs.objects.filter(id=cid).first()
                title = '修改[ %s ]图片' % img_obj.title
                info['title'] = img_obj.title
                info['content'] = img_obj.content
                info['url'] = img_obj.url
                info['img'] = img_obj.img
            else:
                title = '添加图片'
        obj = ImgsForm(initial=info)
        return render(request, 'tmp/imgedit.html', locals())

    def post(self, request, page_id, library_id, cid):
        ip_id = request.POST.get('ip_id')
        il_id = request.POST.get('il_id')
        self.error = []
        if ip_id != page_id and il_id != library_id:
            self.error.append({'msg': '请勿私自修改代码参数，验证不通过！；'})      # 非法用户
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            self.error.append({'msg':'请求页面不存在或已被删除；'})
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            self.error.append({'msg': '请求地址不正确，请勿私自填写地址！'})
        if int(cid) == 0:
            obj,status = self.creat(request)
        else:
            obj,status = self.edit(request,cid)
        if status:
            return redirect('/page/%s/index.html'%page_id)
        return render(request, 'tmp/imgedit.html', locals())

    def creat(self,request):
        status = True
        obj = ImgsForm(request.POST, request.FILES, status=1)
        if obj.is_valid():
            if obj.cleaned_data.get('img'):
                obj.cleaned_data['img'] = self.upimg(obj.cleaned_data['img'])
            else:
                del obj.cleaned_data['img']
            a = Imgs.objects.create(**obj.cleaned_data)
            if not a:
                status = False
                self.error.append({'msg': '数据创建失败'})
        else:
            status = False
            self.error.append({'msg': '图片不能为空，请重新上传！'})
        return obj,status

    def edit(self, request,cid):
        obj = ImgsForm(request.POST, request.FILES)
        if obj.is_valid():
            if obj.cleaned_data.get('img'):
                obj.cleaned_data['img'] = self.upimg(obj.cleaned_data['img'])
            else:
                del obj.cleaned_data['img']
            ret = Imgs.objects.filter(id=cid).update(**obj.cleaned_data)
            status = True if ret else  False
        return obj,status


class PersonnelView(BaseView):

    def get(self, request, page_id, library_id, cid):
        domain_list = Domain.objects.all()
        info = {'ppl_id': page_id, 'pl_id': library_id}
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        if int(cid) == 0:
            title = '添加人员'
        else:
            if Personnel.objects.filter(id=cid).count():
                p_obj = Personnel.objects.filter(id=cid).first()
                title = '修改[ %s ]图片' % p_obj.name
                info['name'] = p_obj.name
                info['ename'] = p_obj.ename
                info['company'] = p_obj.company
                info['position'] = p_obj.position
                info['summary'] = p_obj.summary
                info['pic'] = p_obj.pic
            else:
                title = '添加人员'
        obj = PersonnelForm(initial=info)
        return render(request, 'tmp/personedit.html', locals())

    def post(self, request, page_id, library_id, cid):
        ppl_id = request.POST.get('ppl_id')
        pl_id = request.POST.get('pl_id')
        self.error = []
        if ppl_id != page_id and pl_id != library_id:
            self.error.append({'msg': '请勿私自修改代码参数，验证不通过！；'})      # 非法用户
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            self.error.append({'msg':'请求页面不存在或已被删除；'})
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            self.error.append({'msg': '请求地址不正确，请勿私自填写地址！'})
        if int(cid) == 0:
            operation = request.POST.get('operation',1)
            obj,status = self.creat(request,operation)
        else:
            obj,status = self.edit(request,cid)
        if status:
            return redirect('/page/%s/index.html'%page_id)
        return render(request, 'tmp/personedit.html', locals())

    def creat(self,request,operation):
        status = True
        obj = PersonnelForm(request.POST, request.FILES, status=operation)
        if obj.is_valid():
            if obj.cleaned_data.get('pic'):
                obj.cleaned_data['pic'] = self.upimg(obj.cleaned_data['pic'],status=1)  # 测试环境 1
            a = Personnel.objects.create(**obj.cleaned_data)
            if not a:
                status = False
                self.error.append({'msg': '数据创建失败'})
        else:
            status = False
            self.error.append({'msg': '验证失败,%s'%obj.errors})
        return obj,status

    def edit(self, request,cid):
        obj = PersonnelForm(request.POST, request.FILES)
        if obj.is_valid():
            if obj.cleaned_data.get('pic'):
                obj.cleaned_data['pic'] = self.upimg(obj.cleaned_data['pic'],status=1)
            ret = Personnel.objects.filter(id=cid).update(**obj.cleaned_data)
            if ret:
                status = True
            else:
                status = False

        return obj,status


class ImportPerson(BaseView):
    '''导入人员信息处理函数'''
    def get(self,request,page_id,library_id):
        domain_list = Domain.objects.all()
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        return render(request,'admin/importuser.html',locals())

    def post(self, request, page_id, library_id):
        domain_list = Domain.objects.all()
        data = []
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        file = request.FILES.get('file')
        if file:
            data = self.excel_to_dict(file)
        return render(request,'admin/importuser.html',locals())


def PersonAddAjax(request):
    '''
    数据批量添加接口
    :param request:
    :return:
    '''
    data = {'status':True,'msg':None}
    page_id = request.POST.get('ppl_id')
    library_id = request.POST.get('pl_id')
    if Page.objects.filter(id=page_id).count() == Library.objects.filter(id=library_id).count():
        obj = PersonnelForm(request.POST)
        if obj.is_valid():
            ret = Personnel.objects.create(**obj.cleaned_data)
            if not ret:
                data['status'] = False
                data['msg'] = '创建失败'
        else:
            data['status'] = False
            data['msg'] = '数据验证失败'
    return HttpResponse(json.dumps(data))


def PersonDelAjax(requset,cid):
    '''
    用户删除人员信息处理
    :param requset:
    :param cid: 数据的id
    :return:
    '''
    data = {'status':True,'msg':None}
    token = requset.GET.get('token')
    if token == md5(cid):
        ret = Personnel.objects.filter(id=cid).delete()
        if not ret:
            data['status'] = False
            data['msg'] = '数据删除失败'
    else:
        data['status'] = False
        data['msg'] = '请求验证失败！'
    return HttpResponse(json.dumps(data))


class ArticleView(BaseView):

    def get(self, request, page_id, library_id, cid):
        domain_list = Domain.objects.all()
        info = {'ap_id': page_id, 'al_id': library_id}
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        if int(cid) == 0:
            title = '添加文章'
        else:
            if Article.objects.filter(id=cid).count():
                article_obj = Article.objects.filter(id=cid).first()
                title = '修改[ %s ]文章' % article_obj.name
                info['name'] = article_obj.name
                info['content'] = article_obj.content
                info['author'] = article_obj.author
                info['amount'] = article_obj.amount
                info['summary'] = article_obj.summary
            else:
                title = '添加文章'
        obj = ArticleForm(initial=info)
        return render(request, 'tmp/articledit.html', locals())

    def post(self, request, page_id, library_id, cid):
        print('post-->')
        ap_id = request.POST.get('ap_id')
        al_id = request.POST.get('al_id')
        self.error = []
        if ap_id != page_id and al_id != library_id:
            self.error.append({'msg': '请勿私自修改代码参数，验证不通过！；'})      # 非法用户
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            self.error.append({'msg':'请求页面不存在或已被删除；'})
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            self.error.append({'msg': '请求地址不正确，请勿私自填写地址！'})
        if int(cid) == 0:
            obj,status = self.creat(request)
        else:
            obj,status = self.edit(request,cid)
        if status:
            return redirect('/page/%s/index.html'%page_id)
        return render(request, 'tmp/articledit.html', locals())

    def creat(self,request):
        status = True
        obj = ArticleForm(request.POST, request.FILES, status=1)
        if obj.is_valid():
            if obj.cleaned_data.get('img'):
                obj.cleaned_data['img'] = self.upimg(obj.cleaned_data['img'],status=1)  # 测试环境 1
            else:
                del obj.cleaned_data['img']
            a = Article.objects.create(**obj.cleaned_data)
            if not a:
                status = False
                self.error.append({'msg': '数据创建失败'})
        else:
            status = False
            self.error.append({'msg': '数据验证不通过！'})
        return obj,status

    def edit(self, request,cid):
        obj = ArticleForm(request.POST, request.FILES)
        if obj.is_valid():
            if obj.cleaned_data.get('img'):
                obj.cleaned_data['img'] = self.upimg(obj.cleaned_data['img'])
            else:
                del obj.cleaned_data['img']
            ret = Article.objects.filter(id=cid).update(**obj.cleaned_data)
            status = True if ret else  False

        return obj,status


class HtmlView(BaseView):

    def get(self, request, page_id, library_id, cid):
        domain_list = Domain.objects.all()
        info = {'hp_id': page_id, 'hl_id': library_id}
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        if int(cid) == 0:
            title = '添加HTML代码'
        else:
            if Html.objects.filter(id=cid).count():
                html_obj = Html.objects.filter(id=cid).first()
                title = '修改[ %s ]代码' % html_obj.name
                info['name'] = html_obj.name
                info['html'] = html_obj.html
            else:
                title = '添加HTML代码'
        obj = HtmlForm(initial=info)
        return render(request, 'tmp/htmledit.html', locals())

    def post(self, request, page_id, library_id, cid):
        hp_id = request.POST.get('hp_id')
        hl_id = request.POST.get('hl_id')
        self.error = []
        if hp_id != page_id and hl_id != library_id:
            self.error.append({'msg': '请勿私自修改代码参数，验证不通过！；'})      # 非法用户
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            self.error.append({'msg':'请求页面不存在或已被删除；'})
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            self.error.append({'msg': '请求地址不正确，请勿私自填写地址！'})
        if int(cid) == 0:
            obj,status = self.creat(request)
        else:
            html_obj = Html.objects.filter(id=cid).first()
            obj,status = self.edit(request,cid)
        if status:
            return redirect('/page/%s/index.html'%page_id)
        return render(request, 'tmp/htmledit.html', locals())

    def creat(self,request):
        status = True
        obj = HtmlForm(request.POST, status=1)
        if obj.is_valid():
            a = Html.objects.create(**obj.cleaned_data)
            if not a:
                status = False
                self.error.append({'msg': '数据创建失败'})
        else:
            status = False
            self.error.append({'msg': '数据验证失败！'})
        return obj,status

    def edit(self, request,cid):
        obj = HtmlForm(request.POST)
        if obj.is_valid():
            ret = Html.objects.filter(id=cid).update(**obj.cleaned_data)
            status = True if ret else False
        return obj,status


def upload_kindeditor_img(request):
    '''
    文章的上传图片
    :param request:
    :return:
    '''
    ret = {'error': 0, 'url': '', 'message': '上传成功'}
    if request.method == 'POST':
        print(request.FILES)
        file_obj = request.FILES.get('imgFile')
        if not file_obj:
            ret['error'] = 1
            ret['message'] = '没有内容'
        else:
            upfile = BaseView()
            path = upfile.upimg(file_obj)
            if path:
                ret['url'] = path
    return HttpResponse(json.dumps(ret))


class DomainView(BaseView):

    def get(self,request):
        domain_list = Domain.objects.all()
        obj = DomainForm()
        return render(request,'admin/domain.html',locals())

    def post(self,request):
        domain_list = Domain.objects.all()
        error = ''
        cid = request.POST.get('cid')
        if cid == '0':
            obj = DomainForm(request.POST)
            if obj.is_valid():
                ret = Domain.objects.create(**obj.cleaned_data)
                if not ret: error = '创建网站api失败!'
            else:
                error = '数据验证不通过'
        else:
            obj = DomainForm(request.POST,status=1)
            if obj.is_valid():
                ret = Domain.objects.filter(id=cid).update(**obj.cleaned_data)
                if not ret: error = '更新网站api失败!'
            else:
                error = '数据验证不通过'
        return render(request,'admin/domain.html',locals())


class LibraryView(BaseView):

    def get(self,request):
        domain_list = Domain.objects.all()
        obj = DomainForm()
        return render(request,'admin/library.html',locals())