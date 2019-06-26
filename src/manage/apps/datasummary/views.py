from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user, get_user_model
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from . import models
import crawl
from django.db.models import Count, F
import json
import redis
import codecs
import re
import numpy as np
import pymysql
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from snownlp import sentiment
from snownlp.sentiment import Sentiment



pool = redis.ConnectionPool.from_url('redis://:yourpassword@127.0.0.1/2')
r = redis.StrictRedis(connection_pool=pool)

# 添加session装饰器
def add_session_info(func):
    def wrapper(request):
        if not request.session['user']:
            request.session['user'] = get_user_model().objects.get(username=get_user(request)).username
            request.session['last_login'] = get_user_model().objects.get(username=get_user(request)).last_login.strftime('%Y-%m-%d %H:%M:%S')
            request.session['is_superuser'] = get_user_model().objects.get(username=get_user(request)).is_superuser
            request.session['email'] = get_user_model().objects.get(username=get_user(request)).email
            request.session['is_staff'] = get_user_model().objects.get(username=get_user(request)).is_staff
            request.session['date_joined'] = get_user_model().objects.get(username=get_user(request)).date_joined.strftime('%Y-%m-%d %H:%M:%S')
        return func(request)
    return wrapper



def etl_data(data=''):

    pass

def index(request):
    message=''
    if request.method == 'POST':
        title = request.POST.get('title')[:100]
        content = request.POST.get('content')
        address = request.POST.get('address')[:100]
        report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        contract = request.POST.get('contract')

        s = SnowNLP(content)
        score = s.sentiments
        keywords = s.keywords(3)
        s.summary(3)
        lyric_attribute=''
        if 0 < score < 0.4:
            lyric_attribute='-1'
        elif 0.4 < score < 0.6:
            lyric_attribute='0'
        elif 0.6 < score <= 1.0:
            lyric_attribute='1'
        else:
            lyric_attribute==''

        print(keywords)
        print(score)
        obj = models.ReportEvent(title=title, content=content, keywords=','.join(keywords),report_time=report_time, address=address, lyric_attribute=lyric_attribute, score=str(format(score, '.10f')), contract=contract )
        obj.save()
        message = '舆情事件上报成功！'
    return render(request, 'index.html', locals())


@login_required
@add_session_info
def admin_index(request):
    publicnotice = models.PublicNotice.objects.all().order_by('deal_with')
    reportevent = models.ReportEvent.objects.all().order_by('deal_with')
    lyricalcount = models.DataSummary.objects.count()
    lyricalcategory=models.DataSummary.objects.values('lyric_attribute').annotate(Count('lyric_attribute'))
    positive, neutral, negative = 0, 0, 0
    for l in lyricalcategory:
        if l.get('lyric_attribute') == '1':
            positive = l.get('lyric_attribute__count')
        if l.get('lyric_attribute') == '0':
            neutral = l.get('lyric_attribute__count')
        if l.get('lyric_attribute') == '-1':
            negative = l.get('lyric_attribute__count')
    return render(request, 'admin_index.html', locals())

@login_required
@add_session_info
def taday_lyrical(request):
    datasummary = models.DataSummary.objects.filter(publish_time__gte=datetime.now().date())
    lyricalcount = models.DataSummary.objects.filter(publish_time__gte=datetime.now().date()).count()
    lyricalcategory=models.DataSummary.objects.filter(publish_time__gte=datetime.now().date()).values('lyric_attribute').annotate(Count('lyric_attribute'))    
    positive, neutral, negative = 0, 0, 0
    for l in lyricalcategory:
        if l.get('lyric_attribute') == '1':
            positive = l.get('lyric_attribute__count')
        if l.get('lyric_attribute') == '0':
            neutral = l.get('lyric_attribute__count')
        if l.get('lyric_attribute') == '-1':
            negative = l.get('lyric_attribute__count')
    return render(request, 'taday_lyrical.html', locals())

@login_required
@add_session_info
def taday_report(request):
    reportevent = models.ReportEvent.objects.filter(report_time__gte=datetime.now().date())
    reportcount = models.ReportEvent.objects.filter(report_time__gte=datetime.now().date()).count()
    lyricalcategory=models.ReportEvent.objects.filter(report_time__gte=datetime.now().date()).values('lyric_attribute').annotate(Count('lyric_attribute'))    
    positive, neutral, negative = 0, 0, 0
    for l in lyricalcategory:
        if l.get('lyric_attribute') == '1':
            positive = l.get('lyric_attribute__count')
        if l.get('lyric_attribute') == '0':
            neutral = l.get('lyric_attribute__count')
        if l.get('lyric_attribute') == '-1':
            negative = l.get('lyric_attribute__count')
    return render(request, 'taday_report.html', locals())

@login_required
@add_session_info
def all_lyrical(request):
    datasummary = models.DataSummary.objects.all()
    lyricalcount = models.DataSummary.objects.count()
    lyricalcategory=models.DataSummary.objects.values('lyric_attribute').annotate(Count('lyric_attribute'))  
    positive, neutral, negative = 0, 0, 0
    for l in lyricalcategory:
        if l.get('lyric_attribute') == '1':
            positive = l.get('lyric_attribute__count')
        if l.get('lyric_attribute') == '0':
            neutral = l.get('lyric_attribute__count')
        if l.get('lyric_attribute') == '-1':
            negative = l.get('lyric_attribute__count')
    return render(request, 'all_lyrical.html', locals())

@login_required
@add_session_info
def all_report(request):
    reportevent = models.ReportEvent.objects.all()
    reportcount = models.ReportEvent.objects.all().count()
    lyricalcategory=models.ReportEvent.objects.all().values('lyric_attribute').annotate(Count('lyric_attribute'))    
    positive, neutral, negative = 0, 0, 0
    for l in lyricalcategory:
        if l.get('lyric_attribute') == '1':
            positive = l.get('lyric_attribute__count')
        if l.get('lyric_attribute') == '0':
            neutral = l.get('lyric_attribute__count')
        if l.get('lyric_attribute') == '-1':
            negative = l.get('lyric_attribute__count')
    return render(request, 'all_report.html', locals())

@login_required
@add_session_info
def all_node(request):
    crawl_list = r.keys('crawl_list*')
    crawl_status = r.keys('crawl_status*')
    allcount = len(crawl_list)
    existcount = len(crawl_status)
    deathcount = allcount - existcount
    nodes_list = [json.loads(r.get(n).decode('utf-8').replace("'", '"')) for n in crawl_list]
    status_list = [json.loads(r.get(s).decode('utf-8').replace("'", '"')) for s in crawl_status]

    nodes = [n.get('spider_name') for n in nodes_list if n.get('spider_name')]
    status = [s.get('spider_name') for s in status_list]

    all_node = []
    for n in nodes_list:
        if n.get('spider_name') in status:
            n['status'] = '存活'
        else:
            n['status'] = '宕机'
        all_node.append(n)
    return render(request, 'all_node.html', locals())


@login_required
@add_session_info
def email_record(request):
    emailrecord = models.EmailRecord.objects.all()
    return render(request, 'email_record.html', locals())


@login_required
@add_session_info
def email_user(request):
    department = models.Department.objects.all()
    return render(request, 'email_user.html', locals())

@login_required
@add_session_info
def perspective_extraction(request):
    commentcontent = models.CommentContent.objects.all()
    return render(request, 'perspective_extraction.html', locals())


@login_required
@add_session_info
def media_distribution(request):
    mediafrom=models.DataSummary.objects.values('content_from').annotate(Count('content_from'))
    mediatype=models.DataSummary.objects.values('media_type').annotate(Count('media_type'))

    result_from = 0
    for f in mediafrom:
        result_from += int(f.get('content_from__count'))
    result_type = 0
    for t in mediatype:
        result_type += int(t.get('media_type__count'))
    return render(request, 'media_distribution.html', locals())



@login_required
@add_session_info
def node_overview(request):

    return render(request, 'lyrical_report.html')

@login_required
@add_session_info
def node_info(request):

    return render(request, 'node_info.html')




@login_required
@add_session_info
def mail_center(request):

    return render(request, 'mail_center.html')

@login_required
@add_session_info
def user(request):

    return render(request, 'user.html')

@login_required
@add_session_info
def auth_logout(request):
    logout(request)
    return redirect(reverse('datasummary:auth_login'))

def auth_login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            login(request, user)
            request.session['user'] = get_user(request).username
            request.session['last_login'] = get_user_model().objects.get(username=get_user(request)).last_login.strftime('%Y-%m-%d %H:%M:%S')
            request.session['is_superuser'] = get_user_model().objects.get(username=get_user(request)).is_superuser
            request.session['email'] = get_user_model().objects.get(username=get_user(request)).email
            request.session['is_staff'] = get_user_model().objects.get(username=get_user(request)).is_staff
            request.session['date_joined'] = get_user_model().objects.get(username=get_user(request)).date_joined.strftime('%Y-%m-%d %H:%M:%S')
            return redirect(reverse('datasummary:admin_index'))
        message = '用户名或密码错误'
    return render(request, 'login.html', locals())

@login_required
@add_session_info
def operate(request):

    return render(request, 'operate.html')



@login_required
@add_session_info
def analysis_opinions(request):

    return render(request, 'analysis_opinions.html')


    
@login_required
@add_session_info
def analysis_propagation(request):

    return render(request, 'analysis_propagation.html')

@login_required
@add_session_info
def analysis_audience(request):

    return render(request, 'analysis_audience.html')

@login_required
@add_session_info
def analysis_event(request):

    return render(request, 'analysis_event.html')
@login_required
def page_not_found(request, exception):

    return render(request, '404.html')
