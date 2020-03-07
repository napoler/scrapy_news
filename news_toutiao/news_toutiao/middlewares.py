# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import random
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from selenium.webdriver.chrome.options import Options
import pickle
import os
class SeleniumSpiderMiddleware(object):
    print("使用SeleniumSpiderMiddleware中间件")
    def __init__(self):
        option = Options()
        # option.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path="tools/chromedriver",
                                       chrome_options=option)
        self.set_cook=False
                                       

    def __del__(self):
        self.driver.close()
    def process_request(self, request, spider):
        time.sleep(random.randint(0,5))
        print("request.url",request.url)
        self.driver.get(request.url)
        if request.url!="https://www.toutiao.com/":

            if self.set_cook ==True:
                pass
            else:
                self.set_cookies()
                self.driver.refresh()
                self.set_cook ==True
        # print("页面开始渲染。。。")
        # self.driver.execute_script("scroll(0, 1000);")
        # time.sleep(1)
        rendered_body = self.driver.page_source
        # print("页面完成渲染。。。")
        if request.url=="https://www.toutiao.com/":
            self.get_cookies()

        #self.driver.quit()
        return HtmlResponse(request.url, body=rendered_body, encoding="utf-8")

    def spider_closed(self, spider, reason):
        print('驱动关闭')
        #self.driver.close()
        pass
    def set_cookies(self):
        cookies=self.readCookies()
        # print("保存的cookies",cookies)
        # self.driver.add_cookie(cookies)
        for cookie in cookies:
            # cookie
            # ck={
            #     "domain": "https://www.toutiao.com",
            #     "name":cookie,
            #     "value":cookies[cookie],
            #     "path":'/',
            #     # "secure":True
            #     "expires":None
            #     }
            # print("ck",ck)

            print("cookie",cookie)
            # cookie['expires']=None
            if 'expiry' in cookie:
                # del cookie['expiry']
                cookie['expiry']=int(cookie['expiry'])
            print(cookie)    
            # cookie['domain']="www.toutiao.com"
            # print("cookies",cookies)
            self.driver.add_cookie(cookie)

    def get_cookies(self):
        Cookies = self.driver.get_cookies()
        print(Cookies)
        cookies = {}
        outputPath = open('sgCookies.pickle','wb') #新建一个文件
        pickle.dump(Cookies,outputPath)
        outputPath.close()
        # for itme in Cookies:
        #     print(itme)
        #     cookies[itme['name']] = itme['value']
        #     outputPath = open('sgCookies.pickle','wb') #新建一个文件
        #     pickle.dump(cookies,outputPath)
        #     outputPath.close()
            # return cookies
        print("cookies",cookies)
    def readCookies(self):
        """这是读取cookies的操作"""
        #if have cookies file,use it
        #if not,getCSDNCkooies()
        if os.path.exists('sgCookies.pickle'):
            readPath = open('sgCookies.pickle','rb')
            Cookies = pickle.load(readPath)
            # print(Cookies)
        else:
            Cookies = self.get_cookies()
        return Cookies

class NewsToutiaoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    # print("使用默认中间件")
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class NewsToutiaoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
