from .models import *
from django.forms.forms import Form
from django.forms import fields, widgets
from django.core.exceptions import ValidationError
from pypinyin import lazy_pinyin
import uuid,re

class UserInfoForm(Form):
    name = fields.CharField(required=True,max_length=64, min_length=1, strip=True,)
    email = fields.EmailField(required=True,max_length=64, min_length=6, strip=True,)
    phone = fields.IntegerField(required=True,max_value=11)
    company = fields.CharField(required=True,max_length=128, min_length=1,)
    department = fields.CharField(required=True,max_length=64, min_length=1, strip=True,)
    position = fields.CharField(required=True,max_length=64, min_length=1, strip=True)
    interest = fields.CharField(required=True,max_length=64, min_length=1, strip=True)
    opinion = fields.CharField(required=True,max_length=64, min_length=1, strip=True)

    class Meta:
        module = Contact


class ChangepwdForm(Form):
    oldpassword = fields.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=widgets.PasswordInput(
            attrs={'class': "form-control col-md-7 col-xs-12",
                'placeholder':u"原密码",
            }
        ),
    )
    newpassword1 = fields.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=widgets.PasswordInput(
            attrs={'class': "form-control col-md-7 col-xs-12",
                'placeholder':u"新密码",
            }
        ),
    )
    newpassword2 = fields.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=widgets.PasswordInput(
            attrs={'class': "form-control col-md-7 col-xs-12",
                'placeholder':u"确认密码",
            }
        ),
    )
    def clean(self):
        if not self.is_valid():
            raise ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data


class PageForm(Form):
    pp_id = fields.CharField(widget=widgets.Select())
    name = fields.CharField(required=True, max_length=64, min_length=1, strip=True)
    url = fields.CharField(required=False, max_length=64, min_length=1, strip=True)

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['pp_id'].widget.choices = PageTemplate.objects.all().values_list('id', 'name')


class ImgsForm(Form):
    ip_id = fields.CharField(required=True,widget=widgets.Select(attrs={'class': "hide"}))
    il_id = fields.CharField(required=True,widget=widgets.Select(attrs={'class': "hide"}))
    title = fields.CharField(required=False, max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "标题名称", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    content = fields.CharField(required=False,widget=widgets.Textarea(
        attrs={'class': 'form-control',
               'placeholder': '请在此填写类型内容，没有请为空。',
               'rows': '10',
               'id': 'mycontent'}))
    url = fields.CharField(required=False, max_length=256,strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "url地址", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    img = fields.ImageField(required=False,
                            widget=widgets.FileInput(attrs={'class': "form-control col-md-7 col-xs-12",}))

    def clean_img(self):
        img = self.cleaned_data['img']
        # status 1 创建数据
        if self.status and not img:
            raise ValidationError('图片不能为空')
        if img:
            _,ext = str(img.name).rsplit('.',1)
            if ext not in ('jpg','png','gif'):
                raise ValidationError('图片格式不正确')
        return img
    def clean_title(self):
        val = self.cleaned_data['title']
        if not val:
            val = '%s'%uuid.uuid1()
        return val[:10]

    def __init__(self, *args, **kwargs):
        self.status = kwargs.get('status', 0)
        if kwargs.get('status'):
            del kwargs['status']
        super(ImgsForm, self).__init__(*args, **kwargs)
        self.fields['ip_id'].widget.choices = Page.objects.all().values_list('id', 'name')
        self.fields['il_id'].widget.choices = Library.objects.all().values_list('id', 'name')

    class Meta:
        module = Imgs


class ArticleForm(Form):
    ap_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    al_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    name = fields.CharField(required=False, max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(attrs={'placeholder': "标题名称", 'class': "form-control col-md-7 col-xs-12"}))
    author = fields.CharField(required=True, max_length=64, min_length=1, strip=True,initial='admin',
                            widget=widgets.TextInput(attrs={'placeholder': "作者，默认为admin", 'class': "form-control col-md-7 col-xs-12"}))
    amount = fields.IntegerField(required=True,initial=1,
                            widget=widgets.TextInput(attrs={'class': "form-control col-md-7 col-xs-12"}))
    content = fields.CharField(required=True,widget=widgets.Textarea(
                                attrs={'class': 'form-control','id':'mycontent'}))
    summary = fields.CharField(required=False, widget=widgets.Textarea(
        attrs={'class': 'form-control','rows': '2',
               'placeholder': '如果为空自动截取文字的前200字。'}))
    img = fields.ImageField(required=False,
                            widget=widgets.FileInput(attrs={'class': "form-control col-md-7 col-xs-12", }))

    def clean(self):
        summary = self.cleaned_data.get('summary')
        if not summary:
            self.cleaned_data['summary'] = self.makedata(self.cleaned_data.get('content'))
        return self.cleaned_data

    def makedata(self,data):
        '''处理内容转换成简介'''
        len_ = re.findall(r'<.+>',data)
        for i in len_:
            data = data.replace(i, '')
        data = data.replace('&nbsp;','')
        data = data.strip()
        return data[:200]

    def __init__(self, *args, **kwargs):
        self.status = kwargs.get('status', 0)
        if kwargs.get('status'):
            del kwargs['status']
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['ap_id'].widget.choices = Page.objects.all().values_list('id', 'name')
        self.fields['al_id'].widget.choices = Library.objects.all().values_list('id', 'name')

    class Meta:
        module = Article


class PersonnelForm(Form):
    ppl_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    pl_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    name = fields.CharField(required=True,max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "中文名", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    ename = fields.CharField(required=False,max_length=128, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "姓名全拼", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    company = fields.CharField(required=True,max_length=128, min_length=1,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "公司名称", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    position = fields.CharField(required=True,max_length=128, min_length=1,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "职位名称", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    summary = fields.CharField(required=False,widget=widgets.Textarea(
                                attrs={'class': 'form-control',
                                       'placeholder': '请在此填写人员简介，如无可以不填',
                                       'rows': '10',
                                       'id': 'mycontent'}))
    pic = fields.ImageField(required=False,widget=widgets.FileInput(attrs={'class': "form-control col-md-7 col-xs-12"}))


    def __init__(self, *args, **kwargs):
        try:
            self.status = int(kwargs.get('status', 0))
        except Exception as e:
            self.status = 0
        if kwargs.get('status'):
            del kwargs['status']
        super(PersonnelForm, self).__init__(*args, **kwargs)
        self.fields['ppl_id'].widget.choices = Page.objects.all().values_list('id', 'name')
        self.fields['pl_id'].widget.choices = Library.objects.all().values_list('id', 'name')

    def clean_pic(self):
        '''判读图片的格式是否正确,判断传入是否是批量上传的数据'''
        val = self.cleaned_data['pic']
        if self.status == 2 or not self.status:
            return val
        if val:
            _,ext = str(val.name).rsplit('.',1)
            if ext not in ('jpg','png','gif'):
                raise ValidationError('图片格式不正确')
        else:
            val = ''
        return val

    def clean(self):
        val = lazy_pinyin(self.cleaned_data['name'])
        if self.cleaned_data['ename'] != val:
            self.cleaned_data['ename'] = ''.join(val)
        if not self.cleaned_data['pic']:
            del self.cleaned_data['pic']
        return self.cleaned_data

    class Meta:
        module = Personnel


class HtmlForm(Form):
    hp_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    hl_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    name = fields.CharField(required=True,max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "标题必填项", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    html = fields.CharField(required=False,widget=widgets.Textarea(
                                attrs={'class': 'form-control',
                                       'placeholder': '请输入HTML代码！',
                                       'rows': '10',
                                       'id': 'mycontent'}))


    def __init__(self, *args, **kwargs):
        try:
            self.status = int(kwargs.get('status', 0))
        except Exception as e:
            self.status = 0
        if kwargs.get('status'):
            del kwargs['status']
        super(HtmlForm, self).__init__(*args, **kwargs)
        self.fields['hp_id'].widget.choices = Page.objects.all().values_list('id', 'name')
        self.fields['hl_id'].widget.choices = Library.objects.all().values_list('id', 'name')

    class Meta:
        module = Html


class DomainForm(Form):
    name = fields.CharField(required=True,max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "网站名称，必填项", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    url = fields.URLField(required=True, max_length=64, min_length=1, strip=True,
                            widget=widgets.URLInput(
                                attrs={'placeholder': "网站链接，点击后可以跳转的页面。", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    def clean(self):
        '''验证数据是否重复'''
        name = self.cleaned_data.get('name')
        ret = Domain.objects.filter(name=name).count()
        if self.status and ret:
            del self.cleaned_data['name']
        else:
            if ret:
                raise ValidationError('数据重复')
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        try:
            self.status = int(kwargs.get('status', 0))
        except Exception as e:
            self.status = 0
        if kwargs.get('status'):
            del kwargs['status']
        super(DomainForm, self).__init__(*args, **kwargs)

    class Meta:
        module = Domain


class LibraryForm(Form):
    ptl_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    plugin_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    weight = fields.CharField(required=False,initial=1,
                            widget=widgets.NumberInput(attrs={'class': "form-control col-md-6 col-xs-6"}))
    name = fields.CharField(required=True,max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "模板名称", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    width = fields.CharField(required=True,max_length=64, min_length=1, strip=True,initial='100%',
                            widget=widgets.TextInput(
                                attrs={'placeholder': "容许多宽？不填默认100%", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    height = fields.CharField(required=True,max_length=64, min_length=1, strip=True,initial='100%',
                            widget=widgets.TextInput(
                                attrs={'placeholder': "容许多高？不填默认100%", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    space =fields.CharField(required=True,max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "容许最大上传kb", 'class': "form-control col-md-6 col-xs-6"}
                            ))

    def clean(self):
        '''验证数据是否重复'''
        name = self.cleaned_data.get('name')
        ret = Domain.objects.filter(name=name).count()
        if self.status and ret:
            del self.cleaned_data['name']
        else:
            if ret:
                raise ValidationError('数据重复')
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        try:
            self.status = int(kwargs.get('status', 0))
        except Exception as e:
            self.status = 0
        if kwargs.get('status'): del kwargs['status']
        super(LibraryForm, self).__init__(*args, **kwargs)
        self.fields['ptl_id'].widget.choices = PageTemplate.objects.all().values_list('id', 'name')
        self.fields['plugin_id'].widget.choices = Plugin.objects.all().values_list('id', 'name')

    class Meta:
        module = Library


class PageTemplateForm(Form):
    domain_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    name = fields.CharField(required=True,max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "模板名称", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    img = fields.ImageField(required=False,
                            widget=widgets.FileInput(attrs={'class': "form-control col-md-7 col-xs-12", }))

    def __init__(self, *args, **kwargs):
        try:
            self.status = int(kwargs.get('status', 0))
        except Exception as e:
            self.status = 0
        if kwargs.get('status'):
            del kwargs['status']
        super(PageTemplateForm, self).__init__(*args, **kwargs)
        self.fields['domain_id'].widget.choices = Domain.objects.all().values_list('id', 'name')

    def clean(self):
        '''验证数据是否重复 1是修改 0是创建'''
        if self.status:
            if not self.cleaned_data.get('img'):
                del self.cleaned_data['img']
            return self.cleaned_data
        else:#创建数据
            if not self.cleaned_data.get('img'):
                raise ValidationError('图片不能为空')
        return self.cleaned_data

    class Meta:
        module = PageTemplate

