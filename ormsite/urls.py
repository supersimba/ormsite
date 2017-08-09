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

]
