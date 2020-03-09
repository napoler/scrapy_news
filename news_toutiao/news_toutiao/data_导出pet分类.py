import pymongo
# from albert_pytorch import classify
from html.parser import HTMLParser
# from  tkitMarker import  *
import re
import tkitFile
import tkitText
#这里定义mongo数据

# 这个文件用来构建宠物分类训练数据集
from albert_pytorch import *



client = pymongo.MongoClient("localhost", 27017)
DB = client.scrapy_Toutiao
print(DB.name)
petclass = classify(model_name_or_path='data/petclass/',num_labels=10,device='cuda')
def get_article(id):

    return DB.article.find_one({"_id":id})

def get_keys(data_path=""):
    tjson=tkitFile.Json(file_path=data_path)
    keys=[]
    for it in tjson.auto_load():
        key=tkitText.Text().md5(it['sentence'])
        keys.append(key)
    return list(set(keys))

def add_data(data,path='data/',name="data.json"):
    """
    添加数据样本
    data=[{"keywords": "哈士奇，主人，嚎叫，便是，说明，思考，没有，犬种，原因，新手，", "content": "新手养狗，哈是无忧无的经验和耐心。"}]

    """
    tkitFile.File().mkdir(path)
    data_path=path+name
    tjson=tkitFile.Json(file_path=data_path)

    tjson.save(data)
    return   tjson.auto_load()
def clear_html_re(src_html):
    '''
    正则清除HTML标签
    :param src_html:原文本
    :return: 清除后的文本
    '''
    content = re.sub(r"</?(.+?)>", "", src_html) # 去除标签
    # content = re.sub(r"&nbsp;", "", content)
    dst_html = re.sub(r"\s+", "", content)  # 去除空白字符
    return dst_html

def auto_clear(text):
    txt = HTMLParser().unescape(text) #这样就得到了txt = '<abc>'
    return clear_html_re(txt)
    
i=0
data=[]
for it in  DB.article_list.find({}):

                    # p = rankclass.pre(it['pt'])
                    # if p>0:
                    #     softmax=rankclass.softmax()
    keys=get_keys(data_path="data/classifypet/train.json")
    # print(keys)
    if it['data']['tag']=="news_pet":
        # print(it)
        one =get_article(it['data']['id'])
        if one ==None:
            pass
        else:
            i=i+1
            txt=one['title']+auto_clear(one['content'])
            key=tkitText.Text().md5(txt)
            if key not in keys:
                
                p=petclass.pre(txt[:500])

                if p==1:

                    item={
                    "label":1,
                    "sentence":txt
                    }
                    pass
                else:
                    print(txt[:500])
                    print(p,1)
                    print("已经标记：",i)
                    mp=input("不一致:")
                    try:
                        item={
                        "label":int(mp),
                        "sentence":txt
                        }
                    except:
                        continue
                        pass
                data.append(item)
                keys.append(key)
            # print(one['title'])
            # print(one['title']+auto_clear(one['content']))
    else:
        one =get_article(it['data']['id'])
        if one ==None:
            pass
        else:
            i=i+1
            txt=one['title']+auto_clear(one['content'])
            key=tkitText.Text().md5(txt)
            if key not in keys:

                p=petclass.pre(txt[:500])


                if p==1:
                    print(txt[:500])
                    print(p,0)
                    print("已经标记：",i)
                    mp=input("不一致:")
                    try:
                        item={
                        "label":int(mp),
                        "sentence":txt
                        }
                    except:
                        continue
                        pass
                else:
                    item={
                        "label":0,
                        "sentence":txt
                    }
                data.append(item)
                keys.append(key)
# print(i)
    if i%10==0:
        add_data(data,path='data/classifypet/',name="train.json")
        data=[]
print(len(data))

add_data(data,path='data/classifypet/',name="train.json")