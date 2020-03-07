# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import pprint
# import tiktText
class NewsToutiaoPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        self.DB = client.scrapy_Toutiao
        # print(DB.name)
    def process_item(self, item, spider):
        # print("获取一条00000000000000000000000000000000000000000",item)
        if item.get('atype')=="self_article":
            # print("b111111111111111111111111")
            
            try:
                one={}
                one['data']=item.get('data')

                one["_id"]=item.get('data').get('id')
                # one["title"]=item.get('data').get('title')
                # one["tag"]=item['data']['tag']
                # news_pet
                one['state']="un"
                pprint.pprint(one)
                self.DB.article_list.insert_one(one) 
            except:
                print("保存list失败")
                pass
        elif  item['atype']=="article":
            try:
                one=item['data']
                one["_id"]=item['aid']
                one["title"]=item['data']['title']
                # one["tag"]=item['data']['tag']
                # news_pet
                self.DB.article.insert_one(one) 
                self.DB.article_list.update_one({"_id":one["_id"]},{"state":"Success"})
                print("add")
            except:
                print('err')
                pass
            pass

        return item
