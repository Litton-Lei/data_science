#coding:utf-8
import time
from math import pi, exp, sqrt

import pandas as pd
import pymysql
import scipy.stats as st

con = pymysql.connect(host='106.75.233.242', port=28306, user='leizhen', passwd='b00c482fb32781964a1e',
                      db='mall', charset='utf8')


def pdf(x, mean, var):
    return exp(-(x - mean) ** 2 / (2 * var ** 2)) / sqrt(2 * pi) * var

def cdf(x):
    return st.norm.cdf(x)


date_list = ['2019-03-31', '2019-06-30', '2019-09-30', '2019-12-31', '2020-03-31', '2020-06-30', '2020-09-30',
             '2020-12-31']
platformid_list = [(3, 4, 5, 6), (2, 7)]

writer = pd.ExcelWriter('I:\\新片场\\素材PDF&元数据.xlsx')
for date in date_list:
    for platformid in platformid_list:
        print(date, platformid, end=';')
        time.sleep(5)
        sql = "SELECT R.user_id,R.Rencency,F.Frequency,M.Monetary " \
              "FROM(SELECT user_id, DATEDIFF(R1.Rencency,@date) AS Rencency " \
              "FROM( SELECT user_id ,MAX(create_time) AS Rencency " \
              "FROM `order` " \
              "WHERE `status` =2 " \
              f"AND platform_id IN {platformid} AND create_time BETWEEN DATE_SUB(@date,INTERVAL 365 DAY) AND @date " \
              "GROUP BY user_id " \
              "ORDER BY Rencency DESC) AS R1) AS R LEFT JOIN " \
              "(SELECT user_id, F1.Frequency " \
              "FROM (SELECT user_id ,COUNT(DISTINCT LEFT(create_time,7)) AS Frequency FROM `order` " \
              f"WHERE `status` =2 AND platform_id IN {platformid} " \
              "AND create_time BETWEEN DATE_SUB(@date,INTERVAL 365 DAY) AND @date " \
              "GROUP BY user_id " \
              "ORDER BY Frequency) AS F1) AS F ON R.user_id = F.user_id " \
              "LEFT JOIN (SELECT user_id,M1.Monetary " \
              "FROM (SELECT user_id ,SUM(original_price/100) AS Monetary " \
              "FROM `order` " \
              f"WHERE `status` =2 AND platform_id IN {platformid} " \
              "AND create_time BETWEEN DATE_SUB(@date,INTERVAL 365 DAY) AND @date " \
              "GROUP BY user_id " \
              "ORDER BY Monetary) AS M1) AS M ON R.user_id = M.user_id " \
              f"INNER JOIN (SELECT @date := '{date}') AS date_x ON 1=1"

        df = pd.read_sql(sql=sql, con=con)
        print(df)
        desc = df.describe()
        R_avg = desc.loc['mean', 'Rencency']
        R_std = desc.loc['std', 'Rencency']
        F_avg = desc.loc['mean', 'Frequency']
        F_std = desc.loc['std', 'Frequency']
        M_avg = desc.loc['mean', 'Monetary']
        M_std = desc.loc['std', 'Monetary']

        df['R_pdf'] = df['Rencency'].apply(lambda x: pdf(x, R_avg, R_std))
        df['F_pdf'] = df['Frequency'].apply(lambda x: pdf(x, F_avg, F_std))
        df['M_pdf'] = df['Monetary'].apply(lambda x: pdf(x, M_avg, M_std))



        df.to_excel(writer, sheet_name=str(date)+str(platformid))
        desc.to_excel(writer, sheet_name='desc_'+str(date)+str(platformid))

writer.save()

        # df.to_csv('{}.csv'.format(),encoding='utf-8-sig')
        # print(desc)


