# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import getpass


def login(header, s, username, password):
    logURL = 'http://xuanke.tongji.edu.cn:443/oiosaml/saml/login'
    res = s.get(logURL)
    soup = BeautifulSoup(res.content, 'html.parser')
    jumpURL = soup.meta['content'][6:]
    header['Accept-Encoding']='gzip, deflate, sdch, br'
    res = s.get(jumpURL, headers=header)
    
    soup = BeautifulSoup(res.content,'html.parser')
    logPageURL = 'https://ids.tongji.edu.cn:8443' + soup.form['action']
    res = s.get(logPageURL, headers=header)
    
    data = {'option':'credential','Ecom_User_ID':username,'Ecom_Password':password,'submit':'登录'}
    soup = BeautifulSoup(res.content,'html.parser')
    loginURL = soup.form['action']
    res = s.post(loginURL, headers=header, data=data)
    
    soup = BeautifulSoup(res.content, 'html.parser')
    str = soup.script.string
    str = str.replace('<!--',' ')
    str = str.replace('-->',' ')
    str = str.replace('top.location.href=\'',' ')
    str = str.replace('\';',' ')
    jumpPage2 = str.strip()
    res = s.get(jumpPage2,headers=header)

    soup = BeautifulSoup(res.content, 'html.parser')
    message = {}
    messURL = soup.form['action']
    message['SAMLResponse'] = soup.input['value']
    res = s.post(messURL, headers=header, data=message)
    res = s.get('http://xuanke.tongji.edu.cn/tj_login/index_main.jsp')
    print(u'成功登陆！')


def get_score(header, s, credits, points):
    jumpURL = 'http://xuanke.tongji.edu.cn/tj_login/redirect.jsp'
    data = {
        'link': '/tj_xuankexjgl/score/query/student/cjcx.jsp?qxid=20051013779916$mkid=20051013779901',
        'qxid': '20051013779916',
        'HELP_URL': 'null',
        'MYXSJL': 'null'
    }
    res = s.get(jumpURL, params=data)
    soup = BeautifulSoup(res.content, 'html.parser')
    table = soup.find('table', id='T1')
    trs = table.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if (len(tds) > 5):
            str1 = tds[3].get_text()
            str2 = tds[4].get_text()
            try:
                credits.append(float(str1))
                points.append(float(str2))
            except ValueError:
                pass


if __name__ == '__main__':
    s = requests.session()
    header={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    credits = []
    points = []
    username = input('Please enter your student ID: ')
    password = getpass.getpass('Please enter your password: ')
    get_score(header, s, credits, points)