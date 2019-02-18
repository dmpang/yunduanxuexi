import requests
import re

str = r'居民身份证'
url = r'https://www.tiku88.com/searchAnswer/search/?q=' + str
headers = {
'Host': 'www.tiku88.com',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Referer': 'https://www.tiku88.com/',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'Hm_lvt_2fe2f8f4c7faf558c5be2bf1e1a2d37e=1550467986; Hm_lpvt_2fe2f8f4c7faf558c5be2bf1e1a2d37e=1550467986',
'Cache-Control': 'no-cache'
}

r = requests.get(url, headers=headers)
res = r'style="color: red">(.*?)</span></li>'
daan = re.findall(res, r.text, re.S)
print(daan)