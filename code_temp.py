# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:31:35 2017
@note: 为了便于阅读，将模块的引用就近安置了
@author: lart
"""

# 编码信息，生成请求，打开页面获取内容
from urllib import request
from http import cookiejar
from urllib import parse
from bs4 import BeautifulSoup
import random
import time
import socket

# 用于生成页面网址的函数
def MakeUrl(page):
    """make the next page's url"""
    url = 'http://blog.csdn.net/_1024/commentlist.html?id=15&type=0&ids=&r=0.4097116603695101&page=' + str(page)
    return url

user_agent = r'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
headers = {
'User-Agent': user_agent, 
'Connection': 'keep-alive'}

url = "http://blog.csdn.net/1024.html"

# 登录页面信息
main_url = 'https://passport.csdn.net/account/login'
formdata = {
    "username":"Your name",
    "password":"***",
    "redir":"http://blog.csdn.net/1024.html"
}

cookie = cookiejar.CookieJar()
cookie_support = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(cookie_support)

logingpostdata = parse.urlencode(formdata).encode('utf-8')
req_ligin = request.Request(url=main_url, data=logingpostdata, headers=headers)
response_login = opener.open(req_ligin).read().decode('utf-8')

login_soup = BeautifulSoup(response_login, "html.parser")
jsessionid = login_soup.select("div.user-pass > form")[0]["action"].split(";")[1]
formdata['lt'] = login_soup.select("input[name='lt']")[0]["value"]
formdata['execution'] = login_soup.select("input[name='execution']")[0]["value"]
formdata['_eventId'] = login_soup.select("input[name='_eventId']")[0]["value"]

main_url = main_url + ';' + 'jsessionid' + jsessionid

logingpostdata = parse.urlencode(formdata).encode('utf-8')
req_ligin = request.Request(url=main_url, data=logingpostdata, headers=headers)
response_login = opener.open(req_ligin).read().decode('utf-8')

# 设置等待时间，避免爬取太快
timeout = 3
socket.setdefaulttimeout(timeout)

page = 0
sum = 0
flag = False
# 追加写文件的方式打开文件
with open('程序猿的自白.txt', 'w+', encoding='utf-8') as file:
    while page < 2815:
        page += 1
        req_comment = request.Request(url=MakeUrl(page), headers=headers)

        # 超时重连
        state = False
        while not state:
            try:
                html = request.urlopen(req_comment).read().decode('utf-8')
                state = True
            except socket.timeout:
                state = False

        # 获得评论内容
        soup = BeautifulSoup(html, "html.parser")
        comments = soup.select("div.grid")
        for item in comments:
            text = item.select("div.imgholder > p")[0]
            file.write(text.get_text() + '\n')
        #if flag==False:
        #    print(soup.findAll('script')[0].split(";")[1].split("=")[1])
        #    flag = True
