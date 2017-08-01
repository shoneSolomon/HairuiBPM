from django.db import models


# 主域名
class Domain(models.Model):
    name = models.CharField('域名名称', max_length=64)
    url = models.URLField('域名地址', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '1-域名管理'


# 域名下模板表
class PageTemplate(models.Model):
    domain = models.ForeignKey('Domain')
    name = models.CharField('模板名称', max_length=64)
    img = models.ImageField('分析图', upload_to='page')

    def __str__(self):
        return '%s-%s' % (self.domain, self.name)

    class Meta:
        verbose_name_plural = '2-模板类型'


# 程序插件表
class Plugin(models.Model):
    name = models.CharField('插件名称', max_length=64)
    table = models.CharField('表名称',max_length=64)

    def __str__(self):
        return '%s-%s' % (self.name, self.table)

    class Meta:
        verbose_name_plural = '3-插件库'


# 程序库表
class Library(models.Model):
    ptl = models.ForeignKey('PageTemplate')
    plugin = models.ForeignKey('Plugin')
    weight = models.SmallIntegerField('权重', default=1)
    name = models.CharField('库名称', max_length=64)
    width = models.CharField('宽度', max_length=10, default='100%', null=True, blank=True)
    height = models.CharField('高度', max_length=10, default='100%', null=True, blank=True)
    space = models.IntegerField('空间', default=10000000, null=True, blank=True)

    def __str__(self):
        return '%s-%s' % (self.ptl, self.name)

    class Meta:
        verbose_name_plural = '3-模板库'


class Page(models.Model):
    pp = models.ForeignKey('PageTemplate')
    name = models.CharField('页面名称', max_length=64)
    url = models.CharField('链接', max_length=256)

    def __str__(self):
        return '%s-%s' % (self.pp, self.name)

    class Meta:
        verbose_name_plural = '4-用户页面管理'


class Imgs(models.Model):
    ip = models.ForeignKey('Page')
    il = models.ForeignKey('Library')
    title = models.CharField('标题', max_length=64, null=True)
    content = models.TextField('文本', null=True)
    url = models.CharField('链接', max_length=256, null=True, blank=True)
    img = models.CharField('图片', max_length=255)

    def __str__(self):
        return '%s-%s' % (self.il, self.title)

    class Meta:
        verbose_name_plural = '5-图片信息'


class Video(models.Model):
    vp = models.ForeignKey('Page')
    vl = models.ForeignKey('Library')
    name = models.CharField('标题', max_length=64)
    url = models.CharField('视频地址', max_length=128)

    def __str__(self):
        return '%s-%s' % (self.vl, self.name)

    class Meta:
        verbose_name_plural = '5-视频信息'


class Article(models.Model):
    ap = models.ForeignKey('Page')
    al = models.ForeignKey('Library')
    name = models.CharField('文章名称', max_length=64)
    author = models.CharField('作者', max_length=20, null=True, blank=True, default='admin')
    img = models.CharField('缩略图', max_length=20, null=True)
    amount = models.IntegerField('访问量', default=1, null=True, blank=True)
    summary = models.CharField('简介',max_length=255,null=True )
    content = models.TextField('文章内容')

    def __str__(self):
        return '%s-%s' % (self.al, self.name)

    class Meta:
        verbose_name_plural = '5-文章信息'


class Personnel(models.Model):
    ppl = models.ForeignKey('Page')
    pl = models.ForeignKey('Library')
    name = models.CharField('姓名', max_length=64)
    ename = models.CharField('姓名拼音', max_length=128, null=True)
    company = models.CharField('公司名称', max_length=128, null=True)
    position = models.CharField('职位', max_length=128, null=True)
    pic = models.CharField('头像', max_length=256, null=True)
    summary = models.TextField('简介', null=True)

    def __str__(self):
        return '%s-%s' % (self.pl, self.name)

    class Meta:
        verbose_name_plural = '5-人员信息'


class Html(models.Model):
    hp = models.ForeignKey('Page')
    hl = models.ForeignKey('Library')
    name = models.CharField('名称', max_length=64)
    html = models.TextField('代码')

    def __str__(self):
        return '%s-%s' % (self.hp, self.name)


class Contact(models.Model):
    name = models.CharField('姓名', max_length=32)
    email = models.EmailField('邮箱', unique=True)
    phone = models.CharField('手机', max_length=11, unique=True)
    company = models.CharField('公司', max_length=128, null=True)
    department = models.CharField('部门', max_length=64, null=True)
    position = models.CharField('职位', max_length=64, null=True)
    interest = models.CharField('兴趣', max_length=256, null=True)
    opinion = models.TextField('意见', null=True)
    creat_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = '6-加入我们信息'
        unique_together = ('name', 'phone')

    def __str__(self):
        return '%s-%s' % (self.name, self.phone)
