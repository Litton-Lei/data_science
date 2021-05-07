import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import demjson
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import requests
import tushare as ts
from matplotlib.ticker import AutoMinorLocator
from tqdm import tqdm

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', None)

pro = ts.pro_api('b51897b92ee2f7191add66ebcaa2ec09701a6b8264bca6064b39fe4f')


def get_stock_basic():
    return pro.stock_basic(exchange='', list_status='L', fields='ts_code,'
                                                                'symbol,'
                                                                'name,'
                                                                'area,'
                                                                'industry,'
                                                                'market,'
                                                                'list_date')


def get_company_info():
    company = pro.stock_company(ts_code="", exchange='', fields='ts_code,'
                                                                'chairman,'
                                                                'manager,'
                                                                'secretary,'
                                                                'reg_capital,'
                                                                'setup_date,'
                                                                'province,'
                                                                'city,'
                                                                'employees,'
                                                                'email,'
                                                                'introduction,'
                                                                'website,'
                                                                'office,'
                                                                'main_business')


def get_stock_daily(ts_code, start_date, end_date):
    df = pro.daily(ts_code='600519.SH', start_date='20200708', end_date='20210328')


def get_fuquan_stock(ts_code):
    print(ts_code)
    response = requests.get(
        'http://finance.sina.com.cn/realstock/company/{}/qianfuquan.js?d=2021-03-16'.format(ts_code)).text.split('\n')[
                   0][1:-1]
    rejs = demjson.decode(response)['data']
    df = pd.DataFrame()
    for key, value in rejs.items():
        date = datetime(int(key[1:5]), int(key[6:8]), int(key[9:11]))
        df_1 = pd.DataFrame(data={'date': date, 'price': value}, index=[0])
        df = df.append(df_1, ignore_index=True)

    df.sort_values(by='date', inplace=True, ascending=True)
    return df



def stock_picture(data,ts_code,titel):
    data = data.iloc[-2000:-1, 0:3]
    fig=plt.figure(figsize=(120, 50))
    x = data['date']
    y = data['price'].astype('float')

    plt.plot(x, y,
             linestyle='-',  # 折线类型
             linewidth=2,  # 折线宽度
             color='steelblue',  # 折线颜色
             marker='o',  # 点的形状
             markersize=6,  # 点的大小
             markeredgecolor='black',  # 点的边框色
             markerfacecolor='steelblue')  # 点的填充色)

    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.title('{}_{}股票获利倍率趋势图'.format(ts_code,titel),fontdict={'weight':'normal','size': 72})
    plt.xlabel('日期',fontdict={'weight': 'normal', 'size': 45})
    plt.ylabel('获利倍率',fontdict={'weight': 'normal', 'size': 45})
    ax = plt.gca()
    # 设置日期的显示格式
    date_format = mpl.dates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(date_format)
    # 设置x轴每个刻度的间隔天数
    xlocator = mpl.pyplot.MultipleLocator(90)
    ax.xaxis.set_major_locator(xlocator)
    # 设置y轴每个刻度的间隔天数
    ylocator = mpl.pyplot.MultipleLocator(10)
    ax.yaxis.set_major_locator(ylocator)
    # 刻度值字体大小设置（x轴和y轴同时设置）
    plt.tick_params(labelsize=32)
    # 设置坐标轴主刻度线之间的辅助刻度线
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))  # 每个主刻度线间等分8段
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))  # 每个主刻度线间等分4段
    # 设置网格线
    ax.grid(linestyle="-", linewidth=0.5, color="r", zorder=0)
    # 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且45度倾斜
    fig.autofmt_xdate(rotation=45)
    plt.savefig('I:\\Python\股票图\\{}_{}.png'.format(ts_code,titel))
    return print(titel,'已完成')

def control():
    df = pd.read_csv('I:\\Python\\股票图\\stock.csv',index_col='index')
    for row in tqdm(df.itertuples()):
        ts_code = row[1]
        ts_code_1 = ts_code[0:6]
        ts_code_2 = ts_code[7:9].lower()
        try:
            data = get_fuquan_stock(ts_code=str(ts_code_2)+str(ts_code_1))
            stock_picture(data=data,ts_code=ts_code,titel=str(row[3])+str(row[5]))
        except:
            continue


control()



def send_email(title, content):
    mail_host = 'smtp.163.com'
    # 163用户名
    mail_user = 'pylitton@163.com'
    # 密码(部分邮箱为授权码)
    mail_pass = 'XPJSVKOLCCVMOSPX'
    # 邮件发送方邮箱地址
    sender = 'pylitton@163.com'
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['835086277@qq.com']

    # 设置email信息
    # 邮件内容设置
    message = MIMEText(_text=content, _subtype='plain', _charset='utf-8')
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
