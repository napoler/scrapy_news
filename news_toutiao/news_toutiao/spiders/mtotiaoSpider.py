# -*- coding: utf-8 -*-
import scrapy
from news_toutiao.items import NewsToutiaoItem
import json
# import Terry_toolkit as tkit
import time,os
import random
# from scrapy_selenium import SeleniumRequest
import urllib
import tkitText
import pymongo

class ToutiaoSpider(scrapy.Spider):
    name = 'mtoutiao'
    allowed_domains = ['www.toutiao.com','m.toutiao.com']
    # allowed_domains = ['https://www.ixigua.com']
    # max_time=time.time()-1000*60
    # start_urls = ['https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E6%9F%AF%E5%9F%BA%E7%8A%AC&autoload=true&count=50&en_qc=1&cur_tab=4&from=search_tab&pd=synthesis&timestamp=1583557540918']
    # start_urls = ['https://www.toutiao.com/']
    
    #内容api
    #https://m.toutiao.com/i6709726448871014925/info/?_signature=hX9KuBAR2ynm5roVo3pvXYV.Sq&i=6709726448871014925
    def __init__(self):
        # self.start_urls=["https://www.toutiao.com"]
        self.start_urls=[]
        client = pymongo.MongoClient("localhost", 27017)
        self.DB = client.scrapy_Toutiao

        for it in self.DB.article_list.find({"state":'un'}):
            self.start_urls.append('https://m.toutiao.com/i'+str(it['_id'])+'/info/')
        # print()
        pass
 
    def parse(self, response):
        """深层次采集使用"""

        # print("频道页面")
        # max_time=time.time()-1000*5
        # print("response",response)

        html = response.text
        # print("response.text",response.text)
        json_text=self.replace(html)
        # print("html",json_text)
        data_json= json.loads(json_text)
        # print('data_json',data_json)
        if data_json.get("success")==True:
            item=self.item()
            line=data_json['data']
            # print(line)
            aid=line['url']
            # tkitText.Text.md5()
            aid = aid.replace("http://toutiao.com/group/", "")
            aid = aid.replace("/", "")
            item['data']=line
            item['aid']=aid
            item['atype']="article"
            yield item    


    def item(self):
        """
        所有数据设置为空
        """
        item=NewsToutiaoItem()
        data={}
        for key in item.keys():
            data[key]=''
        return data
    def replace(self,html):
        """去除标签生成json字符串"""
        html = html.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">','')
        html = html.replace('<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">','')
        html = html.replace('</pre></body></html>', '')
        return html