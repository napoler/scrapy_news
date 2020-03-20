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
# petclass = classify(model_name_or_path='data/petclass/',num_labels=2,device='cuda')
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
# def check_model():
#     """
#     对之前的训练数据重新筛选
#     """
#     tjson=tkitFile.Json(file_path="data/classifypet/train.json")
#     # tjson_b=tkitFile.Json(file_path="data/classifypet/train_b.json")
#     a=0
#     b=0
#     data=[]
#     for it in tjson.auto_load():
#         # print(it)
#         a=a+1
#         p=petclass.pre(it['sentence'])
#         if p==it['label']:
#             b=b+1
#         else:
#             print(it['sentence'][:500])
#             print(it['label'])
#             mp=input("不一致:")
#             it['label']=int(mp)
#         data.append(it)
#         print("one",b,a,b/a)     
#     print(b,a,b/a)
#     add_data(data,path='data/classifypet/',name="train_b.json")
# 对之前的训练数据重新筛选
# check_model()
def run():
    """
    运行数据导出为宠物数据
    """
    i=0
    data=[]
    for it in  DB.article.find({}):
        item={}

                        # p = rankclass.pre(it['pt'])
                        # if p>0:
                        #     softmax=rankclass.softmax()
        # keys=get_keys(data_path="data/hot/train.json")
        # print(it)
        if int(it['impression_count'])>2000 or int(it['comment_count'])>5:
            item['label']=1
        else:
            item['label']=0
        

            
        txt=it['title']+"\n"+auto_clear(it['content'])
        print(txt)
        item['sentence']=txt
        data.append(item)
     model = classify(model_name_or_path='./tkitfiles/hot-check', num_labels=2, device='cuda')
    # model
    model.pre(text)
    rank=model.softmax()[1]*100
run()