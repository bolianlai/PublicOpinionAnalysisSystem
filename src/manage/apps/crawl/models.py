from django.db import models
from django.utils.translation import ugettext_lazy as _

class CrawlList(models.Model):
    site_name = models.CharField(verbose_name = _('站点名称'), max_length=20)
    spider_name = models.CharField(verbose_name = _('爬虫名称'), max_length=20)
    redis_key = models.CharField(verbose_name = _('Redis Key'), max_length=20)
    seconds = models.IntegerField(verbose_name = _('状态间隔'))
    datetime = models.DateTimeField(verbose_name = _('更新日期'), blank=True, null=True)
    start_api = models.TextField(verbose_name = _('采集入口'))
    status = models.CharField(verbose_name = _('节点状态'), choices=(('1','存活'),('0','宕机')), max_length=2, blank=True, null=True)
    remark = models.CharField(verbose_name = _('备注'), max_length=20)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = _('采集站点')
        verbose_name_plural = _('采集站点')
