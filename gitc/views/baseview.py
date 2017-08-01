#!/usr/bin/env python     
# -*- coding:utf-8 -*-
#  Author   Hairui
from django.views import View
from gitc.models import Personnel
from pypinyin import lazy_pinyin
from webserver.settings import BASE_DIR, UPKEY, UPURL, UPPORT,IMG_STATUS
import uuid, os, requests, time, hashlib, json, xlrd


class BaseView(View):
    def upimg(self, imgobj,status=IMG_STATUS):
        path, filename = self._recv(imgobj)
        if status:
            return '/static/tmp/%s'%filename
        _, hz = filename.rsplit('.', 1)
        if hz.lower() not in ('jpg', 'gif','png'):
            os.remove(path)
            return False
        if path:
            url = self._up(path, filename)
            return url
        return ''

    def _recv(self, img):
        _, hz = str(img.name).rsplit('.', 1)
        filename = '%s.%s' % (str(uuid.uuid1()), hz)
        img_path = os.path.join(BASE_DIR, 'status', 'tmp', filename)
        with open(img_path, 'wb') as f:
            for data in img.chunks():
                f.write(data)
        return img_path, filename

    def _up(self, path, filename):
        with open(path, 'rb') as f:
            data = f.read()
        if data:
            os.remove(path)
        _url = UPURL % UPPORT
        cookies = {'gitc': 'www.kylinclub.com'}
        files = {'file': (filename, data)}
        rdata = requests.post(_url, files=files, cookies=cookies, data={'token': self._verify(), 't': self.t})
        dic = json.loads(rdata.text)
        if dic.get('status'):
            return dic.get('data')

    def _verify(self):
        self.t = time.time()
        m = hashlib.md5()
        data = '%s-%s' % (self.t, UPKEY)
        m.update(data.encode('utf-8'))
        return m.hexdigest()

    def excel_to_dict(self, file):
        path, filename = self._recv(file)
        _, hz = filename.rsplit('.', 1)
        if hz.lower() not in ('xlsx', 'xls'):
            os.remove(path)
            return []
        if path:
            data = self._read_data(path)
            return data

    def _read_data(self, path):
        data = xlrd.open_workbook(path)
        table = data.sheets()[0]
        nrows = table.nrows  # 行数
        title = ['cid', 'name', 'ename', 'company', 'position', 'summary']
        data = []
        for i in range(nrows):
            # 获取每行数据
            row_val = table.row_values(i)
            if i == 0:
                continue
            tmp = {'status': False, 'data': {}}
            # 将值变成键值对的方式保存
            for index, key in enumerate(title):
                if key == 'ename':
                    val = ''.join(lazy_pinyin(tmp['data'].get('name')))
                else:
                    val = row_val[index]
                tmp['data'][key] = val
            # 数据验证
            if self._data_review(tmp['data']):
                tmp['status'] = True
            else:
                tmp['status'] = False
            data.append(tmp)
        os.remove(path)
        return data

    def _data_review(self, data):
        '''
        数据验证
        :param data:
        :return:
        '''
        cname = data.get('name')
        ename = data.get('ename')
        ret = Personnel.objects.filter(name=cname, ename=ename).count()
        return False if ret else True
