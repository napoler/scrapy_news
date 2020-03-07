# -*- coding: utf-8 -*-
import scrapy
from news_toutiao.items import NewsToutiaoItem
import json
# import Terry_toolkit as tkit
import time,os
import random
# from scrapy_selenium import SeleniumRequest
import urllib
import pprint
from urllib import parse


class ToutiaoSpider(scrapy.Spider):
    name = 'itoutiao'
    allowed_domains = ['www.toutiao.com','m.toutiao.com']
    # allowed_domains = ['https://www.ixigua.com']
    # max_time=time.time()-1000*60
    # start_urls = ['https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E6%9F%AF%E5%9F%BA%E7%8A%AC&autoload=true&count=50&en_qc=1&cur_tab=4&from=search_tab&pd=synthesis&timestamp=1583557540918']
    # start_urls = ['https://www.toutiao.com/']
    
    #内容api
    #https://m.toutiao.com/i6709726448871014925/info/?_signature=hX9KuBAR2ynm5roVo3pvXYV.Sq&i=6709726448871014925
    def __init__(self):
        self.start_urls=["https://www.toutiao.com"]
        if os.path.exists("sgCookies.pickle"):
            #删除文件，可使用以下两种方法。
            os.remove("sgCookies.pickle")
        pass
 
    # def parse_article(self, response):
    #     """深层次采集使用"""
    #     # print("频道页面")
    #     # max_time=time.time()-1000*5
    #     # print("response",response)
    #     html = response.text
    #     print("response.text",response.text)
    #     json_text=self.replace(html)
    #     # print("html",json_text)
    #     data_json= json.loads(json_text)
    #     print('data_json',data_json)
    #     if data_json.get("success")==True:
    #         item=self.item()
    #         for i,line in enumerate( data_json['data']):
    #             # print(line)
    #             aid=line['url']
    #             aid = aid.replace("http://toutiao.com/group/", "")
    #             aid = aid.replace("/", "")
    #             item['data']=line
    #             item['aid']=aid
    #             yield item    
    #     # item=self.item()
    #     # for i,line in enumerate( data_json):  
    #     #     print(line)   
    def auto_offset(self,url,p=20):
        # url = "https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E6%B5%81%E6%B5%AA%E7%8C%AB&count=20&from=search_tab&pd=synthesis&timestamp=1583580720"
        urla = url.split("?")
        # print(urla)
        res = parse.parse_qs(urla[1])
        # print(res)

        new={}
        for k in res.keys():
            if k=='offset':
                new[k]=int(res[k][0])+p
            else:
                new[k]=res[k][0]
        # print(new)
        q=urllib.parse.urlencode(new)
        # print(q)
        return urla[0]+"?"+q
    def parse(self, response):
        """深层次采集使用"""
        # print("频道页面")
        # max_time=time.time()-1000*5
        # print("response",response)
        # print(response.url)
        if response.url=="https://www.toutiao.com":
            pass
        else:
            # print(response.url)
            

            html = response.text
            json_text=self.replace(html)
            # print("html",json_text)

            data_json= json.loads(json_text)

            # print('data_json',data_json)
            if data_json.get("return_count")>0:
                if data_json.get("count")==data_json.get("return_count"):
                    self.start_urls.append(self.auto_offset(response.url,data_json.get("count")))
                item=self.item()
                for i,line in enumerate( data_json['data']):
                    # print("======="*100)
                    # pprint.pprint(line)
                    if line.get('display_type_self'):
                        try:
                            item['data']=line
                            item['atype']= line.get('display_type_self')
                            # pprint.pprint(item)
                            yield item 
                        except:
                            pass
                    # if line.get('display_type_self')=='self_article':
                    #     url="https://m.toutiao.com/i"+line.get('id')+"/info/"
                    #     try:
                    #         yield response.follow(url, callback=self.parse_article)     # it will filter duplication automatically
                            
                    #     except:
                    #         pass

        # item=self.item()
        # for i,line in enumerate( data_json):  
        #     print(line)

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