1、创建项目

        在开始爬取之前，您必须创建一个新的Scrapy项目。进入您打算存储代码的目录中，运行新建命令。

例如，我需要在D:\00Coding\Python\scrapy目录下存放该项目，打开命令窗口，进入该目录，执行以下命令：

scrapy startproject  toutiao

PS:tutorial可以替换成任何你喜欢的名称，最好是英文

      该命令将会创建包含下列内容的 tutorial 目录:

tutorial/
    scrapy.cfg
    tutorial/
        __init__.py
        items.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
            ...

这些文件分别是:

scrapy.cfg: 项目的配置文件

tutorial/: 该项目的python模块。之后您将在此加入代码。

tutorial/items.py: 项目中的item文件.

tutorial/pipelines.py: 项目中的pipelines文件.

tutorial/settings.py: 项目的设置文件.

tutorial/spiders/: 放置spider代码的目录.

 
2、定义Item

        Item 是保存爬取到的数据的容器；其使用方法和python字典类似，并且提供了额外保护机制来避免拼写错误导致的未定义字段错误。我们需要从想要爬取的网站（这里爬取新浪新闻）中获取以下属性：

新闻大类url、新闻大类title；

新闻小类url、新闻小类title；

新闻url、新闻title；

新闻标题、新闻内容；

       对此，在item中定义相应的字段。编辑tutorial目录中的 items.py 文件:

    from scrapy.item import Item, Field
    class TutorialItem(Item):
        # define the fields for your item here like:
        # name = scrapy.Field()
       parent_title = Field()
       parent_url = Field()
     
       second_title = Field()
       second_url = Field()
       path = Field()
     
       link_title = Field()
       link_url = Field()
       head= Field()
       content = Field()
       pass


3、编写爬虫(Spider)

       Spider是用户编写用于从单个网站(或者一些网站)爬取数据的类。

       1、sinaSpider.py文件：

       包含了一个用于下载的初始URL，如何跟进网页中的链接以及如何分析页面中的内容，提取生成 item 的方法。为了创建一个Spider，您必须继承 scrapy.Spider 类，且定义以下三个属性:

name:用于区别Spider。该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。

start_urls:包含了Spider在启动时进行爬取的url列表。因此，第一个被获取到的页面将是其中之一。后续的URL则从初始的URL获取到的数据中提取。

parse() 是spider的一个方法。被调用时，每个初始URL完成下载后生成的Response 对象将会作为唯一的参数传递给该函数。该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的Request 对象。

当我们爬取了大类，然后这时候没有保存item，而是传递item到小类，爬取完小类之后，我们需要去新闻详情页爬取新闻的内容和标题：

主要思路是：paser->second_paser->detail_parse


以下是sinaSpider的全部代码：


    # -*-coding: utf-8 -*-
    __author__= 'George'
    import sys, os
    reload(sys)
    sys.setdefaultencoding("utf-8")
    from scrapy.spider import Spider
    from scrapy.http import Request
    from scrapy.selector import Selector
    from tutorial.items import TutorialItem
    base ="d:/dataset/" #存放文件分类的目录
    class SinaSpider(Spider):
       name= "sina"
       allowed_domains= ["sina.com.cn"]
       start_urls= [
           "http://news.sina.com.cn/guide/"
       ]#起始urls列表
     
       def parse(self, response):
           items= []
           sel= Selector(response)
           big_urls=sel.xpath('//div[@id=\"tab01\"]/div/h3/a/@href').extract()#大类的url
           big_titles=sel.xpath("//div[@id=\"tab01\"]/div/h3/a/text()").extract()
           second_urls =sel.xpath('//div[@id=\"tab01\"]/div/ul/li/a/@href').extract()#小类的url
           second_titles=sel.xpath('//div[@id=\"tab01\"]/div/ul/li/a/text()').extract()
     
           for i in range(1,len(big_titles)-1):#这里不想要第一大类,big_title减去1是因为最后一个大类，没有跳转按钮，也去除
               file_name = base + big_titles[i]
               #创建目录
               if(not os.path.exists(file_name)):
                   os.makedirs(file_name)
               for j in range(19,len(second_urls)):
                   item = TutorialItem()
                   item['parent_title'] =big_titles[i]
                   item['parent_url'] =big_urls[i]
                   if_belong =second_urls[j].startswith( item['parent_url'])
                   if(if_belong):
                       second_file_name =file_name + '/'+ second_titles[j]
                       if(not os.path.exists(second_file_name)):
                           os.makedirs(second_file_name)
                       item['second_url'] = second_urls[j]
                       item['second_title'] =second_titles[j]
                       item['path'] =second_file_name
                       items.append(item)
           for item in items:
               yield Request(url=item['second_url'],meta={'item_1': item},callback=self.second_parse)
     
       #对于返回的小类的url，再进行递归请求
       def second_parse(self, response):
           sel= Selector(response)
           item_1= response.meta['item_1']
           items= []
           bigUrls= sel.xpath('//a/@href').extract()
     
           for i in range(0, len(bigUrls)):
               if_belong =bigUrls[i].endswith('.shtml') and bigUrls[i].startswith(item_1['parent_url'])
               if(if_belong):
                   item = TutorialItem()
                   item['parent_title'] =item_1['parent_title']
                   item['parent_url'] =item_1['parent_url']
                   item['second_url'] =item_1['second_url']
                   item['second_title'] =item_1['second_title']
                   item['path'] = item_1['path']
                   item['link_url'] = bigUrls[i]
                   items.append(item)
           for item in items:
                   yield Request(url=item['link_url'], meta={'item_2':item},callback=self.detail_parse)
     
       def detail_parse(self, response):
           sel= Selector(response)
           item= response.meta['item_2']
           content= ""
           head=sel.xpath('//h1[@id=\"artibodyTitle\"]/text()').extract()
           content_list=sel.xpath('//div[@id=\"artibody\"]/p/text()').extract()
           for content_one in content_list:
               content += content_one
           item['head']= head
           item['content']= content
           yield item


         2、pipelines.py

     主要是对于抓取数据的保存（txt），这里把文件名命名为链接中'/'替换成'_'


    # -*- coding: utf-8 -*-
     
    # Define your item pipelines here
    #
    # Don't forget to add your pipeline to the ITEM_PIPELINES setting
    # See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
    from scrapy import signals
    import json
    import codecs
    import sys
    reload(sys)
    sys.setdefaultencoding( "utf-8" )
    class SinaPipeline(object):
        def process_item(self, item, spider):
            link_url = item['link_url']
            file_name = link_url[7:-6].replace('/','_')
            file_name += ".txt"
            fp = open(item['path']+'/'+file_name, 'w')
            fp.write(item['content'])
            fp.close()
            return item

3、setting.py

    这是设置文件，这里需要设置同时开启的线程数目、日志打印的级别等


    # -*- coding: utf-8 -*-
    BOT_NAME = 'tutorial'
     
    SPIDER_MODULES = ['tutorial.spiders']
    NEWSPIDER_MODULE = 'tutorial.spiders'
    ITEM_PIPELINES = {
        'tutorial.pipelines.SinaPipeline': 300,
    }
    LOG_LEVEL = 'INFO'
    ROBOTSTXT_OBEY = True


 

爬取结果

             这里的文件夹是根据分类，然后创建的；

        这是大类的文件夹，现在我们已经将item都爬下来了，就需要存了，这里只想要存内容，所以直接将item里面的content字段的内容写入txt。

        这里通过将链接进行处理，转换成文件名，最后保存到所属的那个类里；

