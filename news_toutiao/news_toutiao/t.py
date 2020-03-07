from urllib import parse
import urllib

def auto_offset(url,p=20):
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
    return q


url = "https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E6%B5%81%E6%B5%AA%E7%8C%AB&count=20&from=search_tab&pd=synthesis&timestamp=1583580720"

auto_offset(url,p=20)