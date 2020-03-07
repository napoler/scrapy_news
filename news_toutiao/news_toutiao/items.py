# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class ToutiaoItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class NewsToutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    data = scrapy.Field()
    aid = scrapy.Field()
    atype=scrapy.Field()
    pass
