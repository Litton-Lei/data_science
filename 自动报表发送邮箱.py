import datetime
import smtplib
from email.mime.text import MIMEText

import pandas as pd
import pymysql
import requests

print("核心数据自动发送邮箱")


class getFromDataBase():

    def __init__(self):
        self.con_mall = pymysql.connect(host='106.75.233.242', port=28306, user='leizhen',
                                        passwd='b00c482fb32781964a1e',
                                        db='mall', charset='utf8')

    def getNewResourseNum(self):
        sql = "select QUARTER(t.firsttime) 'q', count(*) '新用户数' " \
              "from (select user_id as uid, min(create_time) as firsttime " \
              "from `order` where platform_id in (2,3,4,5,6,7,8,9,11) and status = 2 group by user_id) t " \
              "where t.firsttime >= '2021' " \
              "group by QUARTER(t.firsttime)"
        df_NewResourseNum = pd.read_sql(sql=sql, con=self.con_mall).iat[1, 1]
        return df_NewResourseNum


class getFromSensors():

    def __init__(self):
        self.url = "https://sa.xinpianchang.com/api/sql/query?" \
                   "token=ee33d9f5a116111566847814e7a5acc9f37402245c76c3bf528cf3879a01e725&project=production"

    def get30dMeanDAU(self):
        date1 = (datetime.date.today() - datetime.timedelta(days=30))
        date2 = (datetime.date.today() - datetime.timedelta(days=1))
        print(date1, date2)

        sql1 = "select avg(tb1.num) as avg1 from(select date,count(distinct user_id) as num from events " \
               "where event = '$AppStart' " \
               f"and date between '{date1}' and '{date2}' " \
               "group by date " \
               "order by date) tb1"

        sql2 = "select avg(tb1.num) as avg2 from(select date,count(distinct user_id) as num " \
               "from events where event = '$pageview' " \
               "and $url regexp 'www.xinpianchang.com' " \
               "and $os in ('Mac','Windows') " \
               f"and date between '{date1}' and '{date2}' " \
               "group by date " \
               "order by date) tb1"

        params1 = {
            "q": sql1,
            "format": "json"
        }

        params2 = {
            "q": sql2,
            "format": "json"
        }

        response1 = int(requests.get(url=self.url, params=params1).json()['avg1'])
        response2 = int(requests.get(url=self.url, params=params2).json()['avg2'])

        return response1+response2



def send_email(title, content):
    mail_host = 'smtp.163.com'
    # 163用户名
    mail_user = 'pylitton@163.com'
    # 密码(部分邮箱为授权码)
    mail_pass = 'XPJSVKOLCCVMOSPX'
    # 邮件发送方邮箱地址
    sender = 'pylitton@163.com'
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['leizhen@xinpianchang.com']

    # 设置email信息
    # 邮件内容设置
    message = MIMEText(_text=content, _subtype='html', _charset='utf-8')
    # 邮件主题
    message['Subject'] = title
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]

    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误


def control():
    title = "目标表数据提示邮件_{}".format(datetime.date.today())
    getDataM = getFromDataBase()
    data_NewResourseNum = getDataM.getNewResourseNum()

    getDataS = getFromSensors()
    data_30DAU = getDataS.get30dMeanDAU()

    content = """
    <html>
    <head></head> 
    <body>  
    <p>Q2季度全球精选新增用户数:{}</p>
    <p>最近30天社区日活(app启动+web全站):{}</p>
    </body>  
    </html>  
    """.format(data_NewResourseNum,data_30DAU)
    print(data_NewResourseNum,data_30DAU)
    send_email(title=title, content=content)

control()