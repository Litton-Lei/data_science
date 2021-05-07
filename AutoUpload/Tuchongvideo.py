# -*-coding:utf8 -*-

import os
import pickle
import re
import time
from time import sleep

import pandas as pd
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class login:
    browser = webdriver.Chrome()

    def __init__(self):
        self.loginURL = 'https://contributor.tuchong.com/pr'
        self.homeURL = 'https://contributor.tuchong.com/home'
        self.videouploadurl = 'https://contributor.tuchong.com/contribute?category=2'
        self.delete = 'https://contributor.tuchong.com/mine?status=draft&source=2'
        self.phoneNo = '13080822485'
        self.passWord = '424317030'
        self.saveCookiePath = './cookie/'

    def getCookies(self):
        '''获取cookie'''
        self.browser.get(self.loginURL)
        self.browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/a[2]').click()
        self.browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/input[1]').send_keys(self.phoneNo)
        self.browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/input[2]').send_keys(self.passWord)
        self.browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/label/span[1]/input').click()
        self.browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div[6]').click()
        while True:
            time.sleep(5)
            while self.browser.current_url == self.homeURL:
                XPCCookies = self.browser.get_cookies()
                cookies = {}
                for item in XPCCookies:
                    # print(item['name'], ">>>>>>", item['value'])
                    cookies[item['name']] = item['value']
                savecookie = open(f"{self.saveCookiePath}{self.phoneNo}_tuchong.pickle", mode='wb')
                pickle.dump(cookies, savecookie)
                savecookie.close()
                print(XPCCookies, "\n>>>>>>>>>>>>\n", cookies)
                return cookies

    def readCookies(self):
        '''读取cookie'''
        if os.path.exists(f"{self.saveCookiePath}{self.phoneNo}_=tuchong.pickle"):
            readcookie = open(f"{self.saveCookiePath}{self.phoneNo}_tuchong.pickle", mode='rb')
            cookies = pickle.load(readcookie)
        else:
            if os.path.exists(f'{self.saveCookiePath}'):
                pass
            else:
                os.mkdir(self.saveCookiePath)
            cookies = self.getCookies()
        return cookies

    def login(self):
        '''登陆并到上传页面'''
        cookies = self.readCookies()
        self.browser.get(self.videouploadurl)
        for cookie in cookies:
            self.browser.add_cookie(
                {
                    "domain": "tuchong.com",
                    "name": cookie,
                    "value": cookies[cookie],
                    "path": "/",
                    "expires": None
                }
            )
        self.browser.get(self.videouploadurl)
        sleep(2)



class upload(login):

    def __init__(self):
        super(upload, self).__init__()
        self.videoinfo = 'E:\\videoinfo - pexels.xlsx'
        self.uploadAutoIt = 'C:\\Users\\leily\\Desktop\\python练习\\updown\\picupload.exe "{}"'
        self.path = None
        self.filelist = None
        self.en_name = None
        self.index = None
        self.title = None
        self.cate = None
        self.df_fileInfo = None
        self.tags = []

    def readInfo(self):
        if os.path.exists(self.videoinfo):
            self.df_fileInfo = pd.read_excel(self.videoinfo, index_col='index')
            print(self.df_fileInfo)
            # 选择isxpcupload为空的行
            df_fileInfo_no = self.df_fileInfo[(self.df_fileInfo['isupload'].isnull())
                                              &(self.df_fileInfo['duration']>5)
                                              &(self.df_fileInfo['duration']<60)
                                              &(self.df_fileInfo['resolution']!='1280*720')
                                              &(self.df_fileInfo['resolution']!='720*1280')]
            for row in df_fileInfo_no.itertuples():

                self.index = row[0]
                # self.tags = getattr(row, 'tags')
                self.en_name = getattr(row,'en_name')
                self.title = getattr(row, 'sname')
                self.cate = getattr(row, 'cate')
                self.tags = eval(getattr(row, 'tags'))

                if len(self.tags) < 5:
                    self.tags = self.tags + ['实拍','精致','生活','工作','商业']

                return row
        else:
            return None

    def selectvideoFile(self):
        # 更新当前读取的数据库视频数据
        # self.cleanDraft()
        self.browser.get(self.videouploadurl)
        self.readInfo()
        path = 'E:\\pexels\\'+str(self.cate) + '\\' + str(self.en_name)
        print(path)
        # 点击上传按钮
        self.browser.find_element_by_xpath(
            '//*[@id="root"]/section/section/section/div/div[1]/div[2]/span[2]/div/span/button').click()
        os.system(self.uploadAutoIt.format(path))
        os.system(self.uploadAutoIt.format(path))
        sleep(5)
        while True:
            source=self.browser.page_source
            html = etree.HTML(source)
            de = html.xpath('//*[@id="root"]/section/section/section/div/div[1]/div[5]/div/div[1]/div[1]/div[1]/text()')
            if re.search('上传中', ''.join(de)):
                continue
            else:
                break

        return '>>>>>上传完毕'

    def cleanDraft(self):
        while True:
            try:
                self.browser.get(self.delete)
                sleep(2)
                self.browser.find_element_by_css_selector('#root > section > section > section > main > div.mt20 > ul > li:nth-child(1) > div.contribute__item-img > div > span.contribute__item-img-delete').click()
                sleep(1)
                self.browser.find_element_by_css_selector('body > div:nth-child(3) > div > div.ant-modal-wrap > div > div.ant-modal-content > div > div > div.ant-modal-confirm-btns > button.ant-btn.ant-btn-primary').click()
                sleep(1)
            except Exception as e:
                sleep(1)
                return print('>>>>>草稿全部删除')

    def fillInfo(self):
        '''
        填入视频信息，提交审核
        '''
        # 全选
        sleep(1)
        self.browser.find_element_by_xpath('//*[@id="root"]/section/section/section/div/div[1]/div[2]/span[1]/label/span/input').click()
        sleep(1)
        # 是否独家
        try:
            self.browser.find_element_by_xpath(
                f'//*[@id="root"]/section/section/section/div/div[2]/div[2]/form/div[1]/div[2]/div/span/div/span[2]').click()
        except:
            self.browser.find_element_by_xpath(
                f'//*[@id="root"]/section/section/section/div/div[2]/div[3]/form/div[1]/div[2]/div/span/div/span[2]').click()

        sleep(1)
        # 图片用途
        purpose=self.browser.find_element_by_xpath(
            '//*[@id="VideoForm_property"]/div/div/div')
        ActionChains(self.browser).move_to_element(purpose).click(purpose).perform()
        sleep(2)
        try:
            purpose2=self.browser.find_element_by_xpath(
                '/html/body/div[3]/div/div/div/ul/li[2]')
        except:
            purpose2=self.browser.find_element_by_xpath(
                '/html/body/div[2]/div/div/div/ul/li[2]')
        ActionChains(self.browser).move_to_element(purpose2).click(purpose2).perform()
        sleep(1)

        # 图片分类
        try:
            self.browser.find_element_by_xpath(
                f'//*[@id="root"]/section/section/section/div/div[2]/div[2]/form/div[3]/div[2]/div/span/input').click()
        except:
            self.browser.find_element_by_xpath(
                f'//*[@id="root"]/section/section/section/div/div[2]/div[3]/form/div[3]/div[2]/div/span/input').click()
        sleep(1)
        try:
            self.browser.find_element_by_xpath(
                '/html/body/div[4]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[5]'
            ).click()
            self.browser.find_element_by_xpath(
                '/html/body/div[4]/div/div[2]/div/div[2]/div[3]/button'
            ).click()
        except:
            self.browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[4]'
            ).click()
            self.browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[2]/div/div[2]/div[3]/button'
            ).click()
        sleep(1)

        # 图片标题
        try:
            self.browser.find_element_by_xpath(
                '//*[@id="VideoForm_title"]'
            ).send_keys(self.title)
        except:
            self.browser.find_element_by_xpath(
                '//*[@id="VideoForm_title"]'
            ).send_keys(self.title)
        #  视频说明
        try:
            self.browser.find_element_by_xpath(
                '//*[@id="root"]/section/section/section/div/div[2]/div[2]/form/div[5]/div[2]/div/span/textarea'
            ).send_keys(self.title)
        except:
            self.browser.find_element_by_xpath(
                '//*[@id="root"]/section/section/section/div/div[2]/div[2]/form/div[5]/div[2]/div/span/textarea'
            ).send_keys(self.title)
        sleep(1)

        # 关键词
        try:
            tags=self.browser.find_element_by_css_selector(
                '#root > section > section > section > div > div.contribute__sider > div.contribute__sider-form__wrap '
                '> form > div:nth-child(6) > div.ant-col.ant-form-item-control-wrapper > div > span > '
                'div.contribute-form-model.ant-select.ant-select-enabled > div > div > div '
            )
        except:
            tags=self.browser.find_element_by_xpath(
                '//*[@id="root"]/section/section/section/div/div[2]/div[2]/form/div[6]/div[2]/div/span/div[1]/div/div/div'
            )
        ActionChains(self.browser).move_to_element(tags).double_click(tags).send_keys_to_element(tags,','.join(self.tags)).perform()
        sleep(1)

        # 确认提交
        try:
            self.browser.find_element_by_xpath(
                '/html/body/div/section/section/section/div/div[2]/div[3]/div[1]'
            ).click()
        except:
            self.browser.find_element_by_xpath(
                '//*[@id="root"]/section/section/section/div/div[2]/div[3]/div[1]'
            ).click()
        self.recordLog()
        time.sleep(3)
        return print('>>>>>已提交审核')

    def recordLog(self):
        excel=pd.ExcelWriter(self.videoinfo)
        self.df_fileInfo.loc[self.index,'isupload'] = 'y'
        # self.df_fileInfo.loc[self.index,'tags'] = str(self.tags)
        self.df_fileInfo.to_excel(excel_writer=excel,index=True,index_label='index',encoding='utf-8')
        excel.save()


login = login()
login.login()
up = upload()
# up.readInfo()
# up.recordLog()
up.cleanDraft()
for x in range(100):
    up.selectvideoFile()
    up.fillInfo()
