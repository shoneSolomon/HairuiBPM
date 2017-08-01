from django.shortcuts import HttpResponse
from webserver.settings import TOKEN, UPPORT, UPURL, GITC, UPKEY
from gitc.models import Imgs, Personnel
import json, time, hashlib, os


def reposi(status, data):
    data = {'status': status, 'data': data}
    return HttpResponse(json.dumps(data))


def getpic(request, pictype):
    token = request.GET.get('token', 0)
    if token == TOKEN:
        title = request.GET.getlist('title', 0)
        print('title', title)
        if title == 0:
            dic = list(Imgs.objects.filter(status=0, orgid_id=pictype).values('title', 'content', 'url', 'img'))
        else:
            dic = list(Imgs.objects.filter(status=0, orgid_id=pictype).values(*title))
        return reposi(True, dic)
    else:
        return reposi(False, None)


def getperson(request, meet_id):
    token = request.GET.get('token', 0)
    if token == TOKEN:
        title = request.GET.getlist('title', 0)
        print('title', title)
        if title == 0:
            dic = list(
                Personnel.objects.filter(persontype__meet_id=meet_id, status=0).order_by('-ename').values('cname',
                                                                                                          'ename',
                                                                                                          'company',
                                                                                                          'position',
                                                                                                          'pic',
                                                                                                          'summary'))
        else:
            dic = list(
                Personnel.objects.filter(persontype__meet_id=meet_id, status=0).order_by('-ename').values(*title))
        return reposi(True, dic)
    else:
        return reposi(False, None)


def getmeet(request, meet_id):
    return reposi(True, {})


class ImgView:
    def __init__(self, request):
        self.t = float(request.POST.get('t', 0))
        self.tn = time.time()
        self.k = UPKEY
        self.token = request.POST.get('token')
        self.file = request.FILES.get('file')
        self.path = GITC

    def recv(self):
        if self.file:
            filename = self.file.name
            img_path = os.path.join(GITC, filename)
            with open(img_path, 'wb') as f:
                for data in self.file.chunks():
                    f.write(data)
            return '/static/%s' % filename

    def is_valid(self):
        '''
        数据验证，延时不能超过3秒
        :return:
        '''
        if self.tn - self.t >= 3:
            return False
        m = hashlib.md5()
        data = '%s-%s' % (self.t, self.k)
        m.update(data.encode('utf-8'))
        ret = m.hexdigest()
        if ret != self.token:
            return False
        return True


def imgup(request):
    status = False
    path = ''
    if request.method == 'POST':
        obj = ImgView(request)
        if obj.is_valid():
            path = obj.recv()
            if path: status = True
        else:
            status = False
    return reposi(status, path)
