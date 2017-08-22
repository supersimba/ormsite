#coding:utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from django.core import validators
import datetime

class rep_queue(models.Model):
    rid=models.AutoField(primary_key=True)
    describe=models.CharField(max_length=100,blank=False,verbose_name=u'队列描述')
    src_ip=models.GenericIPAddressField(blank=False,verbose_name=u'源端IP')
    src_path=models.CharField(max_length=100,blank=False,verbose_name=u'源端路径')
    src_ssh_user=models.CharField(max_length=20,blank=False,verbose_name=u'源端ssh用户名')
    src_ssh_pwd = models.CharField(max_length=20, blank=False, verbose_name=u'源端ssh密码')
    src_dbid=models.CharField(max_length=15,blank=False,verbose_name=u'S端数据库sid')
    dbps_port=models.IntegerField(blank=False,verbose_name=u'控制台端口')
    extract_port=models.IntegerField(blank=False,verbose_name=u'分析进程端口')
    tgt_ip=models.GenericIPAddressField(blank=False,verbose_name=u'目标端IP')
    tgt_path = models.CharField(max_length=100, blank=False, verbose_name=u'目标端路径')
    tgt_ssh_user = models.CharField(max_length=20, blank=False, verbose_name=u'目标端ssh用户名')
    tgt_ssh_pwd = models.CharField(max_length=20, blank=False, verbose_name=u'目标端ssh密码')
    tgt_dbid = models.CharField(max_length=15, blank=False, verbose_name=u'T端数据库sid')
    collect_port = models.IntegerField(blank=False, verbose_name=u'接收进程端口')
    add_user=models.CharField(max_length=50,verbose_name=u'添加用户',default=u'......')
    src_script_path=models.CharField(max_length=50,verbose_name=u'S端远程脚本目录',null=True)
    tgt_script_path=models.CharField(max_length=50,verbose_name=u'T端远程脚本目录',null=True)
    add_time=models.DateTimeField(verbose_name=u'信息添加时间',default=datetime.datetime.now)


    # objects=models.Manager()
    # req_queue_objects=ReqQueueManager()

    class Meta:
        db_table='rep_queue'
        verbose_name=u'队列配置表'
        verbose_name_plural=verbose_name


class src_moni_info(models.Model):
    sid=models.AutoField(primary_key=True)
    src_ssh_status = models.IntegerField(verbose_name=u'源端ssh连通状态', default=0)
    src_path_status = models.IntegerField(verbose_name=u'源端目录状态', default=0)
    exec_script_status=models.IntegerField(verbose_name=u'源端远程脚本检测', default=0)
    dbps_cnt=models.IntegerField(verbose_name=u'dbps进程数',null=True)
    capture_cnt=models.IntegerField(verbose_name=u'分析进程数',null=True)
    sender_cnt=models.IntegerField(verbose_name=u'传输进程数',null=True)
    capture_rate=models.CharField(verbose_name=u'分析到的序列号',max_length=20,null=True)
    capture_err=models.CharField(verbose_name=u'分析报错信息',null=True,max_length=100)
    sender_err=models.CharField(verbose_name=u'传输进程报错信息',null=True,max_length=100)
    sync_status=models.IntegerField(verbose_name=u'同步状态',null=True)
    active=models.IntegerField(verbose_name=u'队列动作',null=True)
    queue_id=models.IntegerField(verbose_name=u'队列ID信息',null=False)
    add_time=models.DateTimeField(verbose_name=u'监控信息添加时间',default=datetime.datetime.now)
    class Meta:
        db_table='src_moni_info'
        verbose_name=u'源端监控信息表'
        verbose_name_plural=verbose_name



class tgt_moni_info(models.Model):
    tid=models.AutoField(primary_key=True)
    tgt_ssh_status = models.IntegerField(verbose_name=u'目标端ssh连通状态', default=0)
    tgt_path_status = models.IntegerField(verbose_name=u'目标端目录状态', default=0)
    exec_script_status = models.IntegerField(verbose_name=u'目标端远程脚本目录状态', default=0)
    sync_status= models.IntegerField(verbose_name=u'同步状态',null=True)
    active = models.IntegerField(verbose_name=u'同步动作', null=True)
    collect_cnt = models.IntegerField(verbose_name=u'接收进程数',null=True)
    collect_err = models.CharField(verbose_name=u'接收进程报错信息', null=True, max_length=200)
    loader_s_cnt=models.IntegerField(verbose_name=u'全量加载进程数',null=True)
    loader_r_cnt = models.IntegerField(verbose_name=u'增量加载进程数',null=True)
    loader_s_p_cnt = models.IntegerField(verbose_name=u'全量加载配置进程数', null=True)
    loader_r_p_cnt = models.IntegerField(verbose_name=u'增量加载配置进程数', null=True)
    loader_rate=models.CharField(verbose_name=u'加载进度信息',null=True,max_length=200)
    loader_time=models.CharField(verbose_name=u'加载时间信息',null=True,max_length=200)
    loader_err=models.CharField(verbose_name=u'加载报错信息',null=True,max_length=200)
    queue_id=models.ForeignKey(rep_queue,db_column='queue_id',verbose_name=u'队列ID信息')
    add_time = models.DateTimeField(verbose_name=u'监控信息添加时间', default=datetime.datetime.now)
    class Meta:
        db_table='tgt_moni_info'
        verbose_name=u'目标端监控信息表'
        verbose_name_plural=verbose_name