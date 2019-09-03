#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
import paramiko
import time

class Remote_conn():
    '''
    该脚本用于上传war包到相关主机
    具体操作流程如下：
    先选择选项1，上传指定war文件
    再选择选项2，执行替换war包和重启docker的操作
    如果选择其他数字选项，则程序退出
    '''
    def __init__(self,host,filename,user='root',password='xxxx',port=22):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.filename = filename

    ##上传文件方法
    def sftp_put(self):
        try:
            t = paramiko.Transport((self.host,self.port))
            t.connect(username=self.user,password=self.password)
            sftp = paramiko.SFTPClient.from_transport(t)

            Time = time.strftime('%Y%m%d')
            #获取war包名字
            docname = self.filename
            docname = docname.split('.')[0]

            #备份war包
            print('%s 备份开始...'%self.filename)
            sftp.rename("/home/data/zksc/%s/%s"%(docname,self.filename),"/home/data/zksc/%s/%s.%s"%(docname,self.filename,Time))
            print('%s 备份完成...'%self.filename)
 	    #上传路径为/home/data/zksc/{zksc|family}/
            sftp.put("/home/data/zksc2_2test/webapps/%s"%self.filename,"/home/data/zksc/%s/%s"%(docname,self.filename))
        except Exception as e:
            print(str(e))

    ##ssh登录主机方法
    def ssh_conn(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(hostname=self.host,
                       port=self.port,
                       username=self.user,
                       password=self.password)
        docname = self.filename
        docname = docname.split('.')[0]

        print('连接服务器：%s ...'%self.host)
        print('停止tomcat_%s 服务'%docname)
        stdin,stdout,stderr = client.exec_command('docker stop tomcat_%s'%docname)
        time.sleep(3)

        print('启动tomcat_%s 服务'%docname)
        stdin,stdout,stderr = client.exec_command('docker start tomcat_%s'%docname)
        #print(stdout.read().decode('utf-8'))

        client.close()


if __name__ == '__main__':
    print(Remote_conn.__doc__)
    host = sys.argv[1]
    filename = sys.argv[2]
    c = Remote_conn(host,filename)

    print('*'*10+"开始上传文件"+'*'*10) 
    flag = True
    while flag:
        info = '''
        本脚本提供以下操作：
        1、上传文件操作
        2、执行远程命令操作
        '''
        print(info)
        choice = int(input('请输入需要操作的编号：'))
        if choice == 1:
            print('上传文件%s操作开始'%filename)
            c.sftp_put()
            continue
        elif choice == 2:
            print('远程命令操作')
            c.ssh_conn()
            flag = False
        else:
            print('输入错误，请重新执行脚本操作')
            flag = False
