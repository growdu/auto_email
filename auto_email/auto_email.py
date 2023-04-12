"""Main module."""

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from imapclient import IMAPClient
import json

class auto_email(object): 
    def __init__(self):  # 初始化数据
        self.user = None
        self.passwd = None
        self.prot = None
        self.ssl = None
        self.timeout = None
        self.savepath = None
        self.smtp_server = None
        self.smtp_port = None
        self.dst = None
        self.imap_server = None
        self.debug = None
    
    def read_config(self, file):
        with open(file,'r') as load_f:
            load_dict = json.load(load_f)
            self.user = load_dict["user"]
            self.passwd = load_dict["passwd"]
            self.dst = load_dict["dst"]
            self.imap_server = load_dict["imap_server"]
            self.imap_port = load_dict["imap_port"]
            self.smtp_server = load_dict["smtp_server"]
            self.smtp_port = load_dict["smtp_port"]
            self.debug = load_dict["debug"]
            print("user is " + self.user)
            print("passwd is " + self.passwd)
            print("dst is " + self.dst)
            print("imap_server is " + self.imap_server)
            if self.debug == 1:
                print("enable debug")
            else:
                print("disable debug")

 
    def client(self):  # 链接
        try:
            self.server = IMAPClient(self.serveraddress, self.prot, self.ssl, timeout=self.timeout)
            return self.server
        except BaseException as e:
            return "ERROR: >>> " + str(e)
 
    def login(self):  # 认证
        try:
            self.server.login(self.user, self.passwd)
        except BaseException as e:
            return "ERROR: >>> " + str(e)
 
    def getmaildir(self):  # 获取目录列表 [((), b'/', 'INBOX'), ((b'\\Drafts',), b'/', '草稿箱'),]
        dirlist = self.server.list_folders()
        return dirlist
 
    def getallmail(self):  # 收取所有邮件
        print(self.server)
        self.server.select_folder('INBOX', readonly=True)  # 选择目录 readonly=True 只读,不修改,这里只选择了 收件箱
        result = self.server.search()  # 获取所有邮件总数目 [1,2,3,....] 
        #self.server.search(['FROM', 'cjavapy@qq.com'], charset='UTF-8')
        #self.server.search([u'SINCE', date(2022, 3, 14)])
        print("邮件列表:", result)
        for _sm in result:
            # data = self.server.fetch(_sm, ['ENVELOPE'])
            # size = self.server.fetch(_sm, ['RFC822.SIZE'])
            # print("大小", size)
            # envelope = data[_sm][b'ENVELOPE']
            # print(envelope)
            # subject = envelope.subject.decode()
            # if subject:
            #     subject, de = decode_header(subject)[0]
            #     subject = subject if not de else subject.decode(de)
            # dates = envelope.date
            # print("主题", subject)
            # print("时间", dates)
 
            msgdict = self.server.fetch(_sm, ['BODY[]'])  # 获取邮件内容
            mailbody = msgdict[_sm][b'BODY[]']  # 获取邮件内容
            with open(self.savepath + str(_sm), 'wb') as f:  # 存放邮件内容
                f.write(mailbody)

    def send(self, subject, message,  dst):
        msg = MIMEText(message, 'plain', _charset="utf-8")
        # 邮件主题描述
        msg["Subject"] = subject
        msg['From'] = self.user
        msg['To'] = self.dst
        with SMTP_SSL(host=self.smtp_server,port=self.smtp_port) as smtp:
            # 登录发邮件服务器
            smtp.login(user = self.user, password = self.passwd)
            # 实际发送、接收邮件配置
            smtp.sendmail(from_addr = self.user, to_addrs=dst.split(','), msg=msg.as_string())
            smtp.quit()
        print("will send one email")

    def loop(self):
        print("auto_email enter loop")
        if self.debug == 1:
            print("enable debug,not send real mail")
        else:
            self.send("test", "this is a send test", self.dst)
 
    def close(self):
        self.server.close()