#coding:utf-8
import paramiko


#run_flag:操作类型 0 执行check;1 startup;2 stop;3 clear cache;
#run_flag:操作类型 4 src端vman导出对象;
class SyncOper():
    def __init__(self,ip,path,ssh_u,ssh_p,run_flag):
        self.ip=ip
        self.path=path
        self.ssh_u=ssh_u
        self.ssh_p=ssh_p
        self.run_flag=run_flag
        self.result=''

    def runcmd(self):
        if self.run_flag == '0':
            print 'begin to run cmd of check'
            cli = paramiko.SSHClient()
            cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                cli.connect(self.ip,22,self.ssh_u,self.ssh_p)
                stdin, stdout, stderr = cli.exec_command("sh " + self.path + "/scripts/check")
                outlist=stdout.readlines()
                errlist=stderr.readlines()
                if outlist:
                    for item in outlist:
                        self.result=self.result+item.replace('\n','<br />')
                if errlist:
                    for item in errlist:
                        self.result=self.result+item.replace('\n','<br />')
            except Exception,e:
                print e
                self.result=e
            finally:
                print self.result
                return self.result
        if self.run_flag == '1':
            print 'begin to run cmd of startup'
            cli = paramiko.SSHClient()
            cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                cli.connect(self.ip,22,self.ssh_u,self.ssh_p)
                stdin, stdout, stderr = cli.exec_command("sh " + self.path + "/scripts/startup.sh")
                outlist = stdout.readlines()
                errlist = stderr.readlines()
                if outlist:
                    for item in outlist:
                        self.result = self.result + item.replace('\n', '<br />')
                if errlist:
                    for item in errlist:
                        self.result = self.result + item.replace('\n', '<br />')
            except Exception,e:
                print e
                self.result=e
            finally:
                return self.result
        if self.run_flag == '2':
            print 'begin to run cmd of stop'
            cli = paramiko.SSHClient()
            cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                cli.connect(self.ip,22,self.ssh_u,self.ssh_p)
                stdin, stdout, stderr = cli.exec_command("sh " + self.path + "/scripts/stop_vagentd")
                outlist = stdout.readlines()
                errlist = stderr.readlines()
                if outlist:
                    for item in outlist:
                        self.result = self.result + item.replace('\n', '<br />')
                if errlist:
                    for item in errlist:
                        self.result = self.result + item.replace('\n', '<br />')
            except Exception,e:
                print e
                self.result=e
            finally:
                cli.close()
                return self.result
        if self.run_flag == '3':
            print 'begin to run cmd of clear cache'
            cli = paramiko.SSHClient()
            cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                cli.connect(self.ip,22,self.ssh_u,self.ssh_p)
                stdin, stdout, stderr = cli.exec_command("sh " + self.path + "/scripts/clean_vagentd")
                outlist = stdout.readlines()
                errlist = stderr.readlines()
                if outlist:
                    for item in outlist:
                        self.result = self.result + item.replace('\n', '<br />')
                if errlist:
                    for item in errlist:
                        self.result = self.result + item.replace('\n', '<br />')
            except Exception,e:
                print e
                self.result=e
            finally:
                cli.close()
                return self.result
        if self.run_flag == '4':
            print 'begin to run cmd of export dictionary'
            cli = paramiko.SSHClient()
            cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                cli.connect(self.ip,22,self.ssh_u,self.ssh_p)
                stdin, stdout, stderr = cli.exec_command("sh " + self.path + "/scripts/exp_dic.sh "+self.path)
                outlist = stdout.readlines()
                errlist = stderr.readlines()
                if outlist:
                    for item in outlist:
                        self.result = self.result + item.replace('\n', '<br />')
                if errlist:
                    for item in errlist:
                        self.result = self.result + item.replace('\n', '<br />')
            except Exception,e:
                print e
                self.result=e
            finally:
                cli.close()
                return self.result
        if self.run_flag == '5':
            print 'begin to run cmd of fullsync'
            cli = paramiko.SSHClient()
            cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                cli.connect(self.ip,22,self.ssh_u,self.ssh_p)
                stdin, stdout, stderr = cli.exec_command("sh " + self.path + "/scripts/full_expdata.sh")
                outlist = stdout.readlines()
                errlist = stderr.readlines()
                if outlist:
                    for item in outlist:
                        self.result = self.result + item.replace('\n', '<br />')
                if errlist:
                    for item in errlist:
                        self.result = self.result + item.replace('\n', '<br />')
            except Exception,e:
                print e
                self.result=e
            finally:
                cli.close()
                return self.result
        if self.run_flag == '6':
            print 'begin to edit mapping'
            cli = paramiko.SSHClient()
            cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                cli.connect(self.ip,22,self.ssh_u,self.ssh_p)
                stdin, stdout, stderr = cli.exec_command("cat " + self.path + "/config/mapping.ini")
                outlist = stdout.readlines()
                errlist = stderr.readlines()
                if outlist:
                    for item in outlist:
                        self.result = self.result + item
                if errlist:
                    for item in errlist:
                        self.result = self.result + item
            except Exception,e:
                print e
                self.result=e
            finally:
                cli.close()
                return self.result


    def edit_mapping(self):
        pass