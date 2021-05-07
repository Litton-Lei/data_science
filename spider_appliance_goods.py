import os

import pandas as pd
import requests
from tqdm import tqdm


class spider:

    def __init__(self):
        self.url_goods_head = "http://sjt.admin.sjgo365.com/SJT.Image/XZT/Product/84022564001/800/1.jpg"
        self.url_goods_detail = "http://sjt.admin.sjgo365.com/SJT.Image/XZT/Product/84022564001/Detail/1.jpg"
        self.save_path = "I:\\淘宝店\\商品素材"
        self.info = "I:\淘宝店\商品素材\\商品价格_-1164390972.xlsx"
        self.df_info = None


    def read_info(self):

        self.df_info = pd.read_excel(self.info)
        return self.df_info

    def save_info(self, row_index):
        self.read_info()
        writer = pd.ExcelWriter(self.info)
        self.df_info.loc[row_index,'isdown'] = '已下载'
        self.df_info.to_excel(writer,index=False)
        writer.save()

    def request(self,brandname,name,number):

        for index_1 in range(1,10):
            url_800 = "http://sjt.admin.sjgo365.com/SJT.Image/XZT/Product/{}/800/{}.jpg".format(number,index_1)
            response_800 = requests.get(url=url_800)
            if response_800.status_code == 404 and index_1 == 1:
                return 2
            elif response_800.status_code == 404:
                break
            else:
                name_800 = str(name)+'_head_'+str(index_1)
                self.save_picture(brandname=brandname,goodsname=name,name=name_800,content=response_800.content)

        for index_2 in range(1,50):
            url_detail = "http://sjt.admin.sjgo365.com/SJT.Image/XZT/Product/{}/Detail/{}.jpg".format(number,index_2)
            response_detail = requests.get(url=url_detail)
            if response_detail.status_code == 404:
                break
            else:
                name_detail = str(name) + '_detail_' + str(index_2)
                self.save_picture(brandname=brandname,goodsname=name,name=name_detail,content=response_detail.content)
        return 1


    def save_picture(self,goodsname,brandname,name,content):

        if not os.path.exists(str(self.save_path)+'\\'+str(brandname)):
            os.mkdir(str(self.save_path) + '\\' + str(brandname))

        if not os.path.exists(str(self.save_path)+'\\'+str(brandname)+r'\{}'.format(goodsname)):
            os.mkdir(str(self.save_path)+'\\'+str(brandname)+r'\{}'.format(goodsname))

        with open(str(self.save_path)+'\\'+str(brandname)+r'\{}\{}.jpg'.format(goodsname,name),'wb') as f:
            f.write(content)
            print('已保存'+str(name))




spider = spider()
df_info = spider.read_info()

for row in tqdm(df_info.itertuples()):
    if row[15] == '已下载':
        continue
    name = row[2].replace('*'," ")
    try:
        status = spider.request(brandname=row[6],name=name,number=row[3])
        if status == 1:
            spider.save_info(row[0])
    except Exception as e:
        continue

