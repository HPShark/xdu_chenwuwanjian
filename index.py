import configparser
import os
# 简单邮件传输协议
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

from utils import Utils

class Text(object):


    # 加载配置文件
    def loading(self):
        conf = configparser.ConfigParser()
        conf.read(r'AccountInfo.ini', encoding="utf-8")
        self.username = conf['MESSAGE']['account']
        self.password = conf['MESSAGE']['password']
        self.flag = conf['MESSAGE']['flag']
        self.from_email = conf['MESSAGE']['from_email']
        self.to_email = conf['MESSAGE']['to_email']
        self.key = conf['MESSAGE']['key']
        self. message_file= 'data/upload.txt'
        self.successflag = '失败'

    # 日志
    def logging(self, level, text):
        shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.log = self.log + shijian + "  " + level + "  " + str(text) + "\n"

    def uploadmessage(self):

            # cookie_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + "data" + os.sep + Utils.COOKIE_FILE_NAME
            # print("use username and password to upload message, cookie file is save to " + cookie_file)
            LogInMsg, cookie = Utils.get_cookie_from_login(self.username, self.password)
            if LogInMsg == "ok":
                # cookie = Utils.load_cookie_from_file(cookie_file)
                upload_message = Utils.load_upload_message_file(self.message_file)
                UpLoadMsg = Utils.upload_ncov_message(cookie, upload_message=upload_message)
                if UpLoadMsg == "ok":
                    # print(upload_message)
                    self.logging("INFO",upload_message)
                    self.msg = str(upload_message)
                    self.successflag = '成功'
                else:
                    # print(UpLoadMsg)
                    self.logging("ERROR",UpLoadMsg)
                    self.msg = str(UpLoadMsg)

            else:
                print(LogInMsg)
                self.logging("ERROR",LogInMsg)
                self.msg = str(LogInMsg)


    def send_email(self):

        today_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 设置邮箱的域名
        HOST = 'smtp.qq.com'
        # 设置邮件标题
        SUBJECT = '%s : %s 晨午晚检打卡情况 ' % (self.successflag, today_time)
        # 设置发件人邮箱
        FROM = self.from_email
        # 设置收件人邮箱
        TO = self.to_email  # 可以同时发送到多个邮箱
        message = MIMEMultipart('related')

        # 发送邮件正文到对方的邮箱中
        # with open("log.log", "r") as logfile:  # 打开文件
        #     data = logfile.read()  # 读取文件
        zhengwen = "晨午晚检打卡情况：%s\n" % self.msg
        zhengwen = zhengwen + "\n\n--------日志情况--------\n" + self.log
        # logfile.close()


        my_sender = self.from_email
        my_pass = self.key  # 发件人邮箱密码(当时申请smtp给的口令)
        my_user = self.to_email  # 可以同时发送到多个邮箱


        try:
            msg = MIMEText(zhengwen, 'plain', 'utf-8')
            msg['From'] = formataddr(["晨午检脚本", my_sender])
            # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["填报结果", my_user])
            # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = '%s : %s 晨午晚检打卡情况 ' % (self.successflag, today_time)
            # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            # 发件人邮箱中的SMTP服务器，端口是465
            server.login(my_sender, my_pass)
            # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())
            # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print("邮件发送失败:%s" % Exception)

        print("邮件发送成功")



    def main(self):
        self.log = ""
        try:
            print("正在获取数据")
            self.logging("INFO", "正在获取数据")
            self.loading()

            print("正在填报报表")
            self.logging("INFO", "正在填报报表")
            self.uploadmessage()

            print("要发送的邮件内容")
            self.logging("INFO", "要发送的邮件内容：%s" % self.msg)


        except KeyError:
            print("数据错误，请检查 相关信息.ini")
            self.logging("ERROR", "数据错误，请检查 相关信息.ini")

        except Exception as e:
            print(e)
            print("未知错误")
            self.msg = '！！！ 未知错误 ！！！ 赶快手动填 ！！！'
            self.logging("ERROR", "！！！ 未知错误 ！！！ 赶快手动填 ！！！")

        finally:
            if self.flag == '1':
                self.send_email()
                print("已经执行发送邮件任务")


def main_handler(agrs1,agrs2):
    Text().main()


# Text().main()
