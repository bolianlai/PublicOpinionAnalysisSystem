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
from django.urls import path, include
from . import views

app_name = 'datasummary'
urlpatterns = [
    path('', views.index, name='index'),
    path('admin_index', views.admin_index, name='admin_index'),
    path('taday_lyrical', views.taday_lyrical, name='taday_lyrical'),
    path('taday_report', views.taday_report, name='taday_report'),
    path('all_lyrical', views.all_lyrical, name='all_lyrical'),
    path('all_report', views.all_report, name='all_report'),
    path('all_node', views.all_node, name='all_node'),
    path('email_record', views.email_record, name='email_record'),
    path('email_user', views.email_user, name='email_user'),
    path('perspective_extraction', views.perspective_extraction, name='perspective_extraction'),
    path('media_distribution', views.media_distribution, name='media_distribution'),


    path('node_overview', views.node_overview, name='node_overview'),
    path('node_info', views.node_info, name='node_info'),
    # path('mail_people', views.mail_people, name='mail_people'),
    path('mail_center', views.mail_center, name='mail_center'),
    path('user', views.user, name='user'),
    path('auth_logout', views.auth_logout, name='auth_logout'),
    path('auth_login', views.auth_login, name='auth_login'),
    path('operate', views.operate, name='operate'),
    path('analysis_opinions', views.analysis_opinions, name='analysis_opinions'),
    path('analysis_propagation', views.analysis_propagation, name='analysis_propagation'),
    path('analysis_audience', views.analysis_audience, name='analysis_audience'),
    path('analysis_event', views.analysis_event, name='analysis_event'),
]