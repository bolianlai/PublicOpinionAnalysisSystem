from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.urls import path

import datetime


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

# # 首页页面
# def index(request):

#     return ''


# import os
# from manage.settings import REDIS_URL
# import redis
# pool = redis.ConnectionPool.from_url(REDIS_URL)
# r = redis.StrictRedis(connection_pool=pool)
# # 定时器,定时更新抓取时间间隔
# from apscheduler.schedulers.background import BackgroundScheduler

# sched = BackgroundScheduler()

# @sched.scheduled_job('interval', second = 1)
# def crawl_status():

#     print('crawl_status')
    
#     # q = models.CrawlList.objects.filter(enable=1, interval_remaining__gt=0)
#     # for i in q:
#     #     i.interval_remaining -= 1
#     #     i.save()
#     # logger.debug('Update scheduling time...')

# sched.start()
