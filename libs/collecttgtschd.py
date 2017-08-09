#coding:utf-8
#目标端同步信息采集调度器
from apscheduler.schedulers.blocking import *
import MySQLdb
import logging
import paramiko
import datetime

from checkconfig import check_remote

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='collectschd.log',
                filemode='w')


def GetTgtQueueConfig():
    rows=()
    try:
        logging.info('connect to database')
        db=MySQLdb.connect(host='127.0.0.1',port=3306,user='root',passwd="simba2016",db='monidb')
        c=db.cursor()
        c.execute("select tgt_ip,tgt_path,tgt_ssh_user,tgt_ssh_pwd,tgt_script_path,rid from rep_queue")
        rows=c.fetchall()
    except Exception,e:
        logging.error(e)
    finally:
        db.close()
        return rows
        logging.info('connection of database closed complete!')


def CollectTgtMoniInfo():
    args=GetTgtQueueConfig()
    if len(args)>0:
        for r in args:
            print r
            tgtip = r[0]
            tgtpath = r[1]
            sshuser = r[2]
            sshpwd = r[3]
            scriptpath=r[4]
            logging.info('begin to check connection of ssh :%s' % tgtip)
            check_list=check_remote(tgtip,sshuser,sshpwd,tgtpath,scriptpath)
            ssh_status=check_list[0]
            path_status=check_list[1]
            script_status=check_list[2]
            print "check ip : ",tgtip
            print "check path : ", tgtpath
            print "check scritpath :",scriptpath
            print "list1 :"+str(check_list[0])+"list2 :"+str(check_list[1])+"list3 :"+str(check_list[2])
            if check_list[0] == 1 and check_list[1] == 1 and check_list[2] == 1:
                #配置(ip ssh 脚本目录)检查成功
                print 'begin to exec remote shell[target]',tgtip
                cli = paramiko.SSHClient()
                cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    cli.connect(tgtip, 22, sshuser, sshpwd)
                    print "sh "+scriptpath+"/tgt_collect.sh"
                    stdin, stdout, stderr = cli.exec_command("sh "+scriptpath+"/tgt_collect.sh "+tgtpath)
                    out = stdout.readlines()
                    err=stderr.readlines()
                    print '监控脚本输出信息:',len(out)
                    print out
                    if out:
                        try:
                            conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd="simba2016",
                                                   db='monidb')
                            c = conn.cursor()
                            c.execute(
                                    "insert into tgt_moni_info(tgt_ssh_status,tgt_path_status,script_path_status,sync_status,active,collect_cnt,collect_err,loader_s_cnt,loader_r_cnt,loader_s_p_cnt,loader_r_p_cnt,loader_rate,loader_time,loader_err,queue_id,add_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                        [ssh_status, path_status, script_status, out[10],out[8],
                                         out[0],out[1],out[2],out[3],out[4],out[5],out[9],out[6],out[7],
                                         r[5],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                            conn.commit()
                        except MySQLdb, e:
                            print e
                            conn.rollback()
                        finally:
                            c.close()
                            conn.close()
                except Exception,e:
                    print e
                finally:
                    cli.close()
            else:
                #目录检查未通过,不进行数据采集
                try:
                    conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd="simba2016", db='monidb')
                    c = conn.cursor()
                    c.execute("insert into tgt_moni_info(tgt_ssh_status,tgt_path_status,script_path_status,queue_id,add_time) values(%s,%s,%s,%s,%s)",
                          [ssh_status,path_status,script_status,r[5],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                    conn.commit()
                except MySQLdb,e:
                    print e
                    conn.rollback()
                finally:
                    c.close()
                    conn.close()


schd=BlockingScheduler()
schd.add_job(CollectTgtMoniInfo,'interval',seconds=1)
schd.start()
