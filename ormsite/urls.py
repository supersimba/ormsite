#coding:utf-8
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView

from ormapp.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #
    url(r'^ormlogin/$',TemplateView.as_view(template_name='ormapp/ormlogin.html'),name='ormlogin'),
    url(r'^ormindex/$',ormindex),
    url(r'^ormlogin_action/$',ormlogin_action),
    url(r'^ormlogout/$',ormlogout),

    #
    url(r'^orminfo/$',orminfo),
    url(r'^ormlogs/$',TemplateView.as_view(template_name='ormapp/ormlogs.html'),name='ormlogs'),
    url(r'^ormlogs/(?P<RID>\d+)/(?P<TYPE>\d+)$', display_rep_log, name='ormlogs'),
    #
    url(r'^display_source_info/$',display_source_info),
    url(r'^display_target_info/$',display_target_info),
    #
    url(r'^demo1',TemplateView.as_view(template_name='demo/extends1.html'),name='extends1'),
]
