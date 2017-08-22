#coding:utf-8
#检查ssh连通性,及目录是否存在,文件是否存在
import sys
import paramiko
import os

def check_remote(sship,sshuser,sshpwd,softpath,scriptpath):
    dir_list=[softpath,scriptpath]
    chk_list=[]
    cli=paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        cli.connect(sship, 22, sshuser,sshpwd)
        chk_list.append(1)
        if len(dir_list)==2:
            for l in dir_list:
                print 'begin to check directory :',l
                stdin, stdout, stderr = cli.exec_command("ls -rld "+l)
                err=stderr.readlines()
                print len(err)
                if len(err)>0:
                    chk_list.append(-1)
                else:
                    chk_list.append(1)
            return chk_list
    except:
        #ssh 联通失败
        return [-1,-1,-1]
    finally:
        cli.close()