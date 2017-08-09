#coding:utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import json
import MySQLdb
import datetime
from datetime import date
import paramiko

# Create your views here.

# 解决json接受日期有问题
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime('%Y%m%d %H:%M:%S')
        elif isinstance(obj,date):
            return obj.strftime('%Y%m%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self,obj)


def ormlogin_action(req):
    u = req.POST['username']
    p = req.POST['password']
    user = authenticate(username=u, password=p)
    if user is not None:
        login(req, user)
        return HttpResponseRedirect('/ormindex/')
    else:
        return HttpResponseRedirect('/ormlogin/')


def ormlogout(req):
    logout(req)
    return HttpResponseRedirect('/ormlogin/')


@login_required(login_url='/ormlogin/')
def ormindex(req):
    # u=req.GET['loginuser']
    # print req.user.username
    return render_to_response('ormapp/ormindex.html')
