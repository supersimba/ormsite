#coding:utf-8
#源端同步信息采集调度器
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


def GetSrcQueueConfig():
    rows=()
    try:
        logging.info('connect to database')
        db=MySQLdb.connect(host='127.0.0.1',port=3306,user='root',passwd="simba2016",db='monidb')
        c=db.cursor()
        c.execute("select src_ip,src_path,src_ssh_user,src_ssh_pwd,src_script_path,rid from rep_queue")
        rows=c.fetchall()
        # print rows
    except Exception,e:
        logging.error(e)
    finally:
        db.close()
        return rows
        logging.info('connection of database closed complete!')


def CollectSrcMoniInfo():
    args=GetSrcQueueConfig()
    #print len(args)
    # print args
    # print len(args)
    # print args
    if len(args)>0:
        for r in args:
            #print r
            srcip = r[0]
            srcpath = r[1]
            sshuser = r[2]
            sshpwd = r[3]
            scriptpath=r[4]
            # logging.info('begin to check connection of ssh :%s' % srcip)
            check_list=check_remote(srcip,sshuser,sshpwd,srcpath,scriptpath)
            ssh_status=check_list[0]
            path_status=check_list[1]
            script_status=check_list[2]
            print "check ip : ",srcip
            print "check path : ", srcpath
            print "check scritpath :",scriptpath
            print "list1 :"+str(check_list[0])+"list2 :"+str(check_list[1])+"list3 :"+str(check_list[2])
            if check_list[0]==1 and check_list[1]==1 and check_list[2]==1:
                #全部为1检查通过,否则不进行数据采集
                print 'begin to exec remote shell........................'
                cli=paramiko.SSHClient()
                cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    cli.connect(srcip, 22, sshuser, sshpwd)
                    print "sh "+scriptpath+"/src_collect.sh"
                    stdin, stdout, stderr = cli.exec_command("sh "+scriptpath+"/src_collect.sh "+srcpath)
                    out = stdout.readlines()
                    print len(out[7])
                    print out
                    err=stderr.readlines()
                    if out:
                        try:
                            conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd="simba2016",
                                                   db='monidb')
                            c = conn.cursor()
                            c.execute(
                                "insert into src_moni_info(src_ssh_status,src_path_status,script_path_status,dbps_cnt,capture_cnt,sender_cnt,sync_status,active,capture_err,sender_err,capture_rate,queue_id,add_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[ssh_status, path_status,script_status, out[0].strip("\n"),out[1].strip("\n"),out[2].strip("\n"),out[3].strip("\n"),out[4].strip("\n"),out[5].strip("\n"),out[6].strip("\n"),out[7].strip("\n"),r[5],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
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
                # 检查未通过,不进行数据采集
                try:
                    print 'check is error'
                    print ssh_status
                    conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd="simba2016", db='monidb')
                    c = conn.cursor()
                    c.execute("insert into src_moni_info(src_ssh_status,src_path_status,script_path_status,queue_id,add_time) values(%s,%s,%s,%s,%s)",[ssh_status,path_status,script_status,r[5],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                    #c.execute("insert into src_moni_info(src_ssh_status,src_path_status,script_path_status) values(%s,%s,%s)",[ssh_status,path_status,script_status])
                    conn.commit()
                except Exception,e:
                    print e
                except MySQLdb,e:
                    print e
                    conn.rollback()
                finally:
                    print 'finally............'
                    c.close()
                    conn.close()






schd=BlockingScheduler()
schd.add_job(CollectSrcMoniInfo,'interval',seconds=3)
schd.start()