# -*- coding: utf-8 -*-
import scrapy


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['www.toutiao.com']
    start_urls = ['https://www.toutiao.com']
    start_urls = ['https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E6%9F%AF%E5%9F%BA%E7%8A%AC&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1583559776600']
    def parse(self, response):
        print("返回渲染过的页面内容")
        # print(response.text)
        for sel in response.xpath('//div[@id="app"]//div[contains(@class, "card9")]'):
            title = sel.xpath('.//div[@class="weibo-text"]/text()').extract_first()
            print('标题：', title)
