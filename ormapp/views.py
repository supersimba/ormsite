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

from ormapp.models import *
import libs.syncoper
from libs.viewlog import *
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


@login_required(login_url='/ormlogin/')
def orminfo(req):
    # if req.method=='POST':
    dbobj=rep_queue.objects.all()
    return render_to_response('ormapp/orminfo.html', {'dblist': dbobj})


@login_required(login_url='/ormlogin')
def display_rep_log(req,RID,TYPE):
    dbinfo = rep_queue.objects.get(rid=RID)
    # path sshuser sshpwd
    print type(TYPE)
    if TYPE == '1':
        # print dbinfo.src_path
        return render_to_response('ormapp/ormlogs.html', {
            'side_type': TYPE,
            'path': dbinfo.src_path,
            'ip': dbinfo.src_ip,
            'u': dbinfo.src_ssh_user,
            'p': dbinfo.src_ssh_pwd
        })
    else:
        # print dbinfo.tgt_path
        return render_to_response('ormapp/ormlogs.html', {
            'side_type': TYPE,
            'path': dbinfo.tgt_path,
            'ip': dbinfo.tgt_ip,
            'u': dbinfo.tgt_ssh_user,
            'p': dbinfo.tgt_ssh_pwd
        })


def display_replogs(req,RID,TYPE):
    dbinfo=rep_queue.objects.get(rid=RID)
    #path sshuser sshpwd
    print type(TYPE)
    if TYPE=='1':
        print dbinfo.src_path
        return render_to_response('ormlogs.html',{
            'side_type':TYPE,
            'path':dbinfo.src_path,
            'ip':dbinfo.src_ip,
            'u':dbinfo.src_ssh_user,
            'p':dbinfo.src_ssh_pwd
        })
    else:
        return render_to_response('ormlogs.html', {
            'side_type': TYPE,
            'path': dbinfo.tgt_path,
            'ip': dbinfo.tgt_ip,
            'u': dbinfo.tgt_ssh_user,
            'p': dbinfo.tgt_ssh_pwd
        })

def display_target_info(req):
    rid=req.POST["rid"]
    if req.method=='POST':
        infos=tgt_moni_info.objects.filter(queue_id=rid)
        if infos:
            #print infos.order_by('-tid')[0].tid
            o=infos.order_by('-tid')[0]
            infodic={
                'ssh_status':o.tgt_ssh_status,
                'path_status':o.tgt_path_status,
                'script_status':o.exec_script_status,
                'sync_status':o.sync_status,
                'active':o.active,
                'collect_cnt':o.collect_cnt,
                'collect_err':o.collect_err,
                'loader_s_cnt':o.loader_s_cnt,
                'loader_r_cnt':o.loader_r_cnt,
                'loader_s_p_cnt':o.loader_s_p_cnt,
                'loader_r_p_cnt':o.loader_r_p_cnt,
                'loader_rate':o.loader_rate,
                'loader_time':o.loader_time,
                'loader_err':o.loader_err,
                'add_time':o.add_time,
                'record_flag': '1'
            }
            info_json=json.dumps(infodic,cls=CJsonEncoder)
        else:
            infodic = {
                'ssh_status':'',
                'path_status':'',
                'script_status':'',
                'sync_status':'',
                'active':'',
                'collect_cnt':'',
                'collect_err':'',
                'loader_s_cnt':'',
                'loader_r_cnt':'',
                'loader_s_p_cnt':'',
                'loader_r_p_cnt':'',
                'loader_rate':'',
                'loader_time':'',
                'loader_err':'',
                'add_time':'',
                'record_flag': '-1'
            }
            info_json = json.dumps(infodic, cls=CJsonEncoder)
        return HttpResponse(info_json)


def display_source_info(req):
    rid = req.POST["rid"]
    if req.method=='POST':
        infos=src_moni_info.objects.filter(queue_id=rid)
        if infos:
            #print infos.order_by('-tid')[0].tid
            o=infos.order_by('-sid')[0]
            infodic={
                'ssh_status':o.src_ssh_status,
                'path_status':o.src_path_status,
                'script_status':o.exec_script_status,
                'sync_status':o.sync_status,
                'active':o.active,
                'dbps_cnt':o.dbps_cnt,
                'capture_cnt':o.capture_cnt,
                'sender_cnt':o.sender_cnt,
                'capture_err':o.capture_err,
                'sender_err':o.sender_err,
                'add_time':o.add_time,
                'record_flag':'1'
            }
            print infodic['sync_status']
            info_json=json.dumps(infodic,cls=CJsonEncoder)
        else:
            infodic = {
                'ssh_status': '',
                'path_status': '',
                'script_status': '',
                'sync_status': '',
                'active': '',
                'dbps_cnt': '',
                'capture_cnt': '',
                'sender_cnt': '',
                'capture_err': '',
                'sender_err': '',
                'add_time': '',
                'record_flag': '-1'
            }

            info_json = json.dumps(infodic, cls=CJsonEncoder)
        return HttpResponse(info_json)


#check process
def check_process(req):
    if req.method=='POST':
        result=''
        sshcli=paramiko.SSHClient()
        #print req.POST['ip']
        sshcli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            sshcli.connect(req.POST['ip'], 22, req.POST['u'], req.POST['p'])
            stdin, stdout, stderr = sshcli.exec_command('sh '+req.POST['path']+'/scripts/check')
            outstr=stdout.readlines()
            if outstr:
                for l in outstr:
                    result=result+l.replace('\n','<br />')
                print result
        except Exception,e:
            print 'Exception----->%s' %e
        finally:
            return HttpResponse(result)
            sshcli.close()

#显示日志 信息
def display_log(req):
    if req.method=='POST':
        lv=logviewer(req.POST['ip'], req.POST['path'], req.POST['u'], req.POST['p'],req.POST['logname'])
        return HttpResponse(lv.getlog_content())


#复制 操作
def sync_oper(req):
    if req.method=='POST':
        ip=req.POST['ip']
        path=req.POST['path']
        u=req.POST['u']
        p=req.POST['p']
        run_flag=req.POST['runflag']
        runobj=SyncOper(ip,path,u,p,run_flag)
        run_result=runobj.runcmd()
        print 'view :run_result'
        print run_result
        return HttpResponse(run_result)


def edit_mapping(req):
    if req.method=='POST':
        pass