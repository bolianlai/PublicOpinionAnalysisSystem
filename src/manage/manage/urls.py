"""manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from datasummary import views
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('datasummary.urls', namespace='datasummary'))
    # path('', views.index, name='index'),
    # path('lyrical_taday', views.lyrical_taday, name='lyrical_taday'),
    # path('lyrical_monitor/<str:category>/', views.lyrical_monitor, name='lyrical_monitor'),
    # path('lyrical_addtask', views.lyrical_addtask, name='lyrical_addtask'),
    # path('lyrical_early', views.lyrical_early, name='lyrical_early'),
    # path('lyrical_attention', views.lyrical_attention, name='lyrical_attention'),
    # path('lyrical_setting', views.lyrical_setting, name='lyrical_setting'),
    # path('lyrical_report', views.lyrical_report, name='lyrical_report'),
    # path('node_overview', views.node_overview, name='node_overview'),
    # path('node_info', views.node_info, name='node_info'),
    # path('mail_record', views.mail_record, name='mail_record'),
    # path('mail_people', views.mail_people, name='mail_people'),
    # path('mail_center', views.mail_center, name='mail_center'),
    # path('user', views.user, name='user'),
    # path('auth_logout', views.auth_logout, name='auth_logout'),
    # path('auth_login', views.auth_login, name='auth_login'),
    # path('operate', views.operate, name='operate'),
    # path('analysis_trend', views.analysis_trend, name='analysis_trend'),
    # path('analysis_opinions', views.analysis_opinions, name='analysis_opinions'),
    # path('analysis_media', views.analysis_media, name='analysis_media'),
    # path('analysis_propagation', views.analysis_propagation, name='analysis_propagation'),
    # path('analysis_audience', views.analysis_audience, name='analysis_audience'),
    # path('analysis_event', views.analysis_event, name='analysis_event'),
    # path('static/', serve, {'document_root': settings.STATIC_ROOT}),  
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = '舆情分析系统-后台'
admin.site.site_title = '舆情分析系统'
admin.site.index_title = '舆情分析系统'

def page_not_found(request, exception):
    return render(request, '404.html')

from django.shortcuts import render
handler404 = page_not_found

