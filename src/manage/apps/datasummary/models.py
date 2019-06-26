from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Organization(models.Model):
    organization_name = models.CharField(verbose_name = _('组织名称'), max_length=100)
    remark = models.CharField(verbose_name = _('组织备注'), max_length=200, blank = True, null=True)


    def __str__(self):
        return self.organization_name

    class Meta:
        verbose_name = _('组织名称')
        verbose_name_plural = _('组织名称')


class Department(models.Model):
    department_name = models.CharField(verbose_name = _('部门名称'), max_length=100)
    department_owner = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization', verbose_name = _('部门归属'), blank = True)
    notice_email = models.EmailField(verbose_name = _('通知邮箱'))
    register_time = models.DateTimeField(verbose_name = _('注册时间'))
    contract = models.CharField(verbose_name = _('联系方式'), max_length=100)
    address = models.CharField(verbose_name = _('联系地址'), max_length=100, blank = True)
    remark = models.CharField(verbose_name = _('备注'), max_length=200, blank = True, null=True)


    def __str__(self):
        return self.department_name

    class Meta:
        verbose_name = _('部门管理')
        verbose_name_plural = _('部门管理')




class DataSummary(models.Model):
    title = models.CharField(verbose_name = _('舆情名称'), max_length=100)
    intro = models.CharField(verbose_name = _('舆情摘要'), max_length=200)
    content_url = models.CharField(verbose_name = _('舆情链接'), max_length=200)
    content_from = models.CharField(verbose_name = _('舆情来源'), max_length=20)
    media_type = models.CharField(verbose_name = _('媒体类型'), max_length=10)
    lyric_attribute = models.CharField(verbose_name = _('舆情属性'), choices=(('1','正面'),('0','中立'),('-1','反面')), max_length=2, blank=True, null=True)
    publish_time = models.DateTimeField(verbose_name = _('发表时间'))
    update_time = models.DateTimeField(verbose_name = _('采集时间'))
    correlation = models.FloatField(verbose_name = _('关联度'))
    summary = models.ManyToManyField(Department, verbose_name = _('通知部门'), related_name='summary', blank=True, null=True)
    remark = models.CharField(verbose_name = _('备注'), max_length=200, blank = True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('舆情汇总')
        verbose_name_plural = _('舆情汇总')

class ReportEvent(models.Model):
    title = models.CharField(verbose_name = _('舆情名称'), max_length=100)
    content = models.TextField(verbose_name = _('舆情内容'))
    keywords = models.CharField(verbose_name = _('关键词'), max_length=100, blank=True, null=True )
    report_time = models.DateTimeField(verbose_name = _('上报时间'))
    address = models.CharField(verbose_name = _('舆情地点'), max_length=100)
    lyric_attribute = models.CharField(verbose_name = _('舆情属性'), choices=(('1','正面'),('0','中立'),('-1','反面')), max_length=2, blank=True, null=True)
    score = models.CharField(verbose_name = _('舆情评分'), max_length=40, blank=True, null=True)
    contract = models.CharField(verbose_name = _('联系方式'), max_length=100, blank=True, null=True)
    deal_with = models.BooleanField(verbose_name = _('是否已处理'), default= False)
    user = models.ForeignKey(User, verbose_name=_("处理人员"), on_delete=models.CASCADE, related_name='reportevents', blank=True, null=True)
    remark = models.CharField(verbose_name = _('备注'), max_length=200, blank = True, null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('上报舆情')
        verbose_name_plural = _('上报舆情')
    




class PublicNotice(models.Model):
    title = models.CharField(verbose_name = _('舆情名称'), max_length=100)
    intro = models.CharField(verbose_name = _('舆情摘要'), max_length=200)
    report_time = models.DateTimeField(verbose_name = _('通知时间'))
    notices = models.ManyToManyField(Department, verbose_name = _('通知部门'), related_name='notice', blank=True)
    deal_with = models.BooleanField(verbose_name = _('是否已处理'), default= False)
    deal_with_time = models.DateTimeField(verbose_name = _('处理时间'), blank=True, null=True)
    department = models.ManyToManyField(Department, verbose_name=_("处理部门"), related_name='dealwiths', blank=True)
    remark = models.CharField(verbose_name = _('备注'), max_length=200, blank = True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('舆情通知')
        verbose_name_plural = _('舆情通知')



class EmailRecord(models.Model):
    title = models.CharField(verbose_name = _('舆情名称'), max_length=100)
    intro = models.CharField(verbose_name = _('舆情摘要'), max_length=200)
    report_time = models.DateTimeField(verbose_name = _('通知时间'))
    notices = models.TextField(verbose_name = _('通知部门'))
    remark = models.CharField(verbose_name = _('备注'), max_length=200, blank = True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('邮件记录')
        verbose_name_plural = _('邮件记录')

class CommentContent(models.Model):
    title = models.CharField(verbose_name = _('舆情名称'), max_length=100)
    comment = models.TextField(verbose_name = _('评论内容'), max_length=200, blank = True, null=True)
    commentary = models.TextField(verbose_name = _('评论观点'), max_length=200, blank = True, null=True)
    remark = models.CharField(verbose_name = _('备注'), max_length=200, blank = True, null=True)
    update_time = models.DateTimeField(verbose_name = _('更新时间'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('内容评论')
        verbose_name_plural = _('内容评论')