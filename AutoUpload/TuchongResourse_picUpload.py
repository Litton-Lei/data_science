# -*-coding:utf8 -*-

import os
import pickle
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
        self.videouploadurl = 'https://contributor.tuchong.com/contribute?category=0'
        self.delete = 'https://contributor.tuchong.com/mine?status=draft&source='
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
        self.browser.get(self.homeURL)
        for cookie in cookies:
            print(cookie)
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
        self.videoinfo = 'Q:\\Litton 素材辞典 - 副本.xlsx'
        self.uploadAutoIt = 'C:\\Users\\leily\\Desktop\\python练习\\updown\\picupload.exe "{}"'
        self.path = None
        self.filelist = None
        self.index = None
        self.title = None
        self.df_fileInfo = None
        self.tags = []

    def readInfo(self):
        if os.path.exists(self.videoinfo):
            self.df_fileInfo = pd.read_excel(self.videoinfo, index_col='index')
            # 选择isxpcupload为空的行
            df_fileInfo_no = self.df_fileInfo[self.df_fileInfo['isupload'].isnull()]
            for row in df_fileInfo_no.itertuples():

                self.index = row[0]
                # self.tags = getattr(row, 'tags')
                self.path = getattr(row,'path')
                self.title = getattr(row, 'title')
                self.filelist = eval(getattr(row, 'content'))
                print(self.index,self.title)
                return row
        else:
            return None

    def selectvideoFile(self):
        # 更新当前读取的数据库视频数据
        self.cleanDraft()
        self.readInfo()
        for file in self.filelist:
            path = self.path + '\\' + file
            print(path)
            # 点击上传按钮
            self.browser.find_element_by_xpath(
                '/html/body/div[1]/section/section/section/div/div[1]/div[2]/span[2]/div/span/button').click()
            os.system(self.uploadAutoIt.format(path))
            os.system(self.uploadAutoIt.format(path))
            time.sleep(1)
        sleep(5)
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
                self.browser.get(self.videouploadurl)
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
        '//*[@id="ImageForm_property"]/div/div'

        purpose=self.browser.find_element_by_xpath(
            '//*[@id="ImageForm_property"]/div/div')
        ActionChains(self.browser).move_to_element(purpose).perform()
        ActionChains(self.browser).click(purpose).perform()
        sleep(2)
        try:
            purpose2=self.browser.find_element_by_xpath(
                '/html/body/div[2]/div/div/div/ul/li[2]')
        except:
            purpose2=self.browser.find_element_by_xpath(
                '/html/body/div[3]/div/div/div/ul/li[2]')
        ActionChains(self.browser).move_to_element(purpose2).perform()
        ActionChains(self.browser).click(purpose2).perform()
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
                '/html/body/div[4]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[4]'
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

        # 图片说明
        try:
            self.browser.find_element_by_xpath(
                '//*[@id="root"]/section/section/section/div/div[2]/div[2]/form/div[4]/div[2]/div/span/textarea'
            ).send_keys(self.title)
        except:
            self.browser.find_element_by_xpath(
                '//*[@id="root"]/section/section/section/div/div[2]/div[3]/form/div[4]/div[2]/div/span/textarea'
            ).send_keys(self.title)

        sleep(1)
        # 关键词
        try:
            tagc=self.browser.find_element_by_xpath(
                '//*[@id="root"]/section/section/section/div/div[2]/div[2]/form/div[5]/div[2]/div/span/div[1]/div/div/div'
            )
        except:
            tagc=self.browser.find_element_by_xpath(
                '//*[@id="root"]/section/section/section/div/div[2]/div[3]/form/div[5]/div[2]/div/span/div[1]/div/div/div'
            )
        ActionChains(self.browser).move_to_element(tagc).double_click(tagc).perform()
        sleep(1)
        x = 1
        source=self.browser.page_source
        html = etree.HTML(source)
        tags = ['高端', '精致', '自然', '逼格', '高清']
        while True:
            self.tags = tags
            try:
                tag = html.xpath('//*[@id="root"]/section/section/section/div/div[2]/div[2]/form/div[5]/div['
                                 '2]/div/span/div[4]/div/div/div[2]/div/div/div/span[{}]/text()'.format(str(x)))
            except:
                tag = html.xpath('//*[@id="root"]/section/section/section/div/div[2]/div[3]/form/div[5]/div['
                                 '2]/div/span/div[4]/div/div/div[2]/div/div/div/span[{}]/text()'.format(str(x)))
            tags = tags + tag
            x = x+1
            print(self.tags)
            if self.tags == tags:
                break

        ActionChains(self.browser).move_to_element(tagc).send_keys(','.join(self.tags)).perform()

        # 确认提交
        try:
            self.browser.find_element_by_xpath(
                '//*[@id="root"]/section/section/section/div/div[2]/div[3]/div[1]'
            ).click()
        except:
            self.browser.find_element_by_xpath(
                '//*[@id="root"]/section/section/section/div/div[2]/div[4]/div[1]'
            ).click()
        self.recordLog()
        time.sleep(3)
        return print('>>>>>已提交审核')

    def recordLog(self):
        excel=pd.ExcelWriter(self.videoinfo)
        print(self.df_fileInfo)
        self.df_fileInfo.loc[self.index,'isupload'] = 'y'
        self.df_fileInfo.loc[self.index,'tags'] = str(self.tags)
        print(self.df_fileInfo.head(5))
        self.df_fileInfo.to_excel(excel_writer=excel,index=True,index_label='index',encoding='utf-8')
        excel.save()

    # def fillInfo(self):
    #     '''
    #     填入视频信息，提交审核
    #     '''
    #     while True:
    #         sourse = self.browser.page_source
    #         html = etree.HTML(sourse)
    #         state = html.xpath(
    #             '//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div/span/text()')
    #         print(state)
    #         if re.search("上传已完成", "".join(state)):
    #             # 点击填写信息
    #             self.browser.find_element_by_xpath(
    #                 f'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[4]/button').click()
    #             sleep(1)
    #
    #             # 添加输入标题
    #
    #             self.browser.find_element_by_xpath(
    #                 '//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[2]/div/div/input').clear()
    #             self.browser.find_element_by_xpath(
    #                 '//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[2]/div/div/input').send_keys(
    #                 self.zh_name)
    #
    #             while True:
    #                 self.browser.find_element_by_xpath(
    #                     f'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[7]/div/button[3]').click()
    #                 html = etree.HTML(self.browser.page_source)
    #                 Title_tip = html.xpath(
    #                     '//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[2]/div/div[2]/text()')
    #                 if re.search("标题最多20个汉字或40个英文字母", "".join(Title_tip)):
    #                     self.browser.find_element_by_xpath(
    #                         f'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[2]/div/div/input').send_keys(
    #                         Keys.BACKSPACE)
    #                 elif re.search("标题最少4个汉字或8个英文字母", "".join(Title_tip)):
    #                     self.browser.find_element_by_xpath(
    #                         f'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[2]/div/div/input').send_keys(
    #                         "大气磅礴科技商业模板")
    #                 else:
    #                     break
    #
    #             # 输入标签
    #             self.browser.find_element_by_xpath(
    #                 f'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[3]/div/div[1]/input').send_keys(
    #                 self.tags)
    #             sleep(1)
    #
    #             # 选择类别
    #             @retry(stop_max_attempt_number=3, wait_fixed=10000)
    #             def cate():
    #                 type = self.browser.find_element_by_xpath(
    #                     f'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[4]/div[1]/div/div/div[2]/span/span/i')
    #                 ActionChains(self.browser).move_to_element(type).perform()
    #                 ActionChains(self.browser).click(on_element=type).perform()
    #                 sleep(1)
    #                 cateid_1 = self.browser.find_element_by_xpath(
    #                     f'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[4]/div[1]/div/div/div[3]/div[1]/div[1]/ul/li[1]')
    #                 ActionChains(self.browser).move_to_element(cateid_1).perform()
    #                 ActionChains(self.browser).click().perform()
    #                 sleep(1)
    #                 cateid_2 = self.browser.find_element_by_xpath(
    #                     f'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[4]/div[1]/div/div/div[3]/div[1]/div[1]/ul/li[6]')
    #                 ActionChains(self.browser).move_to_element(cateid_2).perform()
    #                 ActionChains(self.browser).click().perform()
    #                 return
    #
    #             try:
    #                 cate()
    #             except Exception as e:
    #                 logging.error(e)
    #                 cate()
    #
    #             # 输入价格
    #             def price():
    #                 type = self.browser.find_element_by_xpath(
    #                     f'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[4]/div[2]/div/div/div[1]/input')
    #                 ActionChains(self.browser).move_to_element(type).perform()
    #                 ActionChains(self.browser).click(on_element=type).perform()
    #                 sleep(1)
    #                 cateid_1 = self.browser.find_element_by_xpath(
    #                     f'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[4]/div[2]/div/div/div[2]/div[1]/div[1]/ul/li[1]')
    #                 ActionChains(self.browser).move_to_element(cateid_1).perform()
    #                 ActionChains(self.browser).click().perform()
    #                 return
    #
    #             try:
    #                 price()
    #             except Exception as e:
    #                 logging.error(e)
    #                 price()
    #
    #             # 确认提交
    #             self.browser.find_element_by_xpath(
    #                 f'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[5]/div/div[2]/form/div[7]/div/button[3]').click()
    #
    #             self.recordLog()
    #             time.sleep(3)
    #             return print('>>>>>已提交审核')
    #
    #         elif re.search(r"失败|网络异常", "".join(state)):
    #             # 删除上传失败的文件
    #             delete = self.browser.find_element_by_css_selector(
    #                 '#__layout > div > div:nth-child(2) > div > div > div.manage-main.no-border > div > div.video-upload-wrapper > div > div.video-upload-list > div > div.video-upload-control > svg')
    #             ActionChains(self.browser).move_to_element(delete).perform()
    #             ActionChains(self.browser).click(on_element=None).perform()
    #             self.browser.find_element_by_xpath('/html/body/div[4]/div/div[3]/button[2]').click()
    #             sleep(3)
    #             # 重新调用上传模块
    #             self.uploadFile()
    #             self.fillInfo()
    #         else:
    #             pass




login = login()
login.login()
up = upload()
# up.readInfo()
# up.recordLog()
up.selectvideoFile()
up.fillInfo()
