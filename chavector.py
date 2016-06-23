#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
Created on 2015-03-03-2015-03-05

@author: zhang&*&*&

'''


'''
非正常的url 包含ip


端口非80

url中的点数量 过多


域名年龄

《emmed》

指向外域链接的比例 空域


是否有ICP声明

在Search engine中的搜索结果


获取的内容统一为unicode编码


__init__: 

初始化，获取网页资源，并创建beautifulsoup对象

'''
import os
from datetime import datetime
from urllib2 import Request, urlopen, URLError, HTTPError
from bs4 import BeautifulSoup,NavigableString
import jieba.analyse
from datetime import date
import re
import chardet
import socket
socket.setdefaulttimeout(30) 
from urlparse import urlparse

#判断含有字符串的标签       
def surrounded_by_strings(tag):
        return (isinstance(tag.next_element, NavigableString)
            and isinstance(tag.previous_element, NavigableString)) and tag.name!="script" and tag.name!="style"


class chavector:

    def __init__(self,url1):
        self.localurl=url1
        self.domain=None
        self.soup=None
        req = Request(url1)
        try:
            response = urlopen(req)
        except URLError , e :
            if isinstance(e.reason, socket.timeout):
               return None
            print "network meets some problems: "
            print "Reason: ",e.reason
            return None
        except ValueError, e:
            print "unknown url type:" ,self.localurl
        else:
            if response!=None:
                    #redirected = response.geturl() == self.url
                    #print redirected
                    the_page = response.read()
                    #print the_page
                    char = chardet.detect(the_page)
                    #解码为unicode
                    the_page.decode(char['encoding'],'ignore')
                    self.soup = BeautifulSoup(the_page)
                    print 'soup success ----',self.localurl
        finally:
            print 'init  end ---- ',self.localurl



    #非正常的url 包含ip
    def geturlip(self):
       m = re.search(r'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))', self.localurl)
       if m:
           return 1
       else:
           return -1

    #@符号

    def geturlat(self):
       m = re.search(r'@', self.localurl)
       if m:
           return 1
       else:
           return -1

    #端口非80
    def getport(self):
        o=urlparse(self.localurl)
        if o.port==None:
            return -1
        elif o.port!=80:
            return 1
        

    #url中的点数量 过多 5个
    def geturldot(self):
        dotnum=0
        for u in self.localurl:
            if u=='.':
                dotnum+=1
        if dotnum>5:
            return 1
        else:
            return -1


    #域名年龄
    '''
     <div id="whoisinfo" class="div_whois">
        注册商：GODADDY.COM, LLC<br/>
        域名服务器：whois.godaddy.com<br/>
        DNS服务器：DNS1.FREEHOSTIA.COM<br/>
        DNS服务器：DNS2.FREEHOSTIA.COM<br/>
        域名状态：运营商设置了客户禁止删除保护<br/>
        域名状态：运营商设置了客户禁止续费保护<br/>
        域名状态：运营商设置了客户禁止转移保护<br/>
        域名状态：运营商设置了客户禁止修改保护<br/>
        更新时间：2012年05月28日<br/>
        创建时间：2012年05月23日<br/>
        过期时间：2013年05月23日<br/>
        联系人：zhu, alice<br/>
        联系方式：<img src="/displayemail.aspx?email=M8N8oc1O|iQhqGCDHdpH9m77v2qrQfW8"/>
        <br/>
        <br/>
    </div>
     '''

    def getdomainage(self):
        o=urlparse(self.localurl)
        #print o.netloc
        domain='http://whois.chinaz.com/'+o.netloc
        #print domain

        req = Request(domain)
        try:
            response = urlopen(req)
            #print response.geturl()
        except URLError , e :
            if isinstance(e.reason, socket.timeout):
                print 'socket timeout'
              
            print "network meets some problems: "
            print "Reason: ",e.reason
            
        else:
            if response!=None:
                the_page = response.read()
                #print the_page
                char = chardet.detect(the_page)
                #解码为unicode
                the_page.decode(char['encoding'],'ignore')
                soup = BeautifulSoup(the_page)
                #<div class="div_whois">
                # print(soup.prettify())
                domain=soup.find('div',id="whoisinfo")
                domain=unicode(domain)
                print 'domain',domain
                #re.search(ur"[\u4e00-\u9fa5]",domain)
                ma= re.search(ur"\u521b\u5efa\u65f6\u95f4.*",domain)
                if ma:
                    string=ma.group()
                    type2=re.search(u"T",string)
                    if type2:
                        print 'T'
                        year= string[6:10]
                        month=string[11:13]
                        day=string[14:16]
                        print year,month,day
                    else:
                        type3=re.search(ur"\u6708-",string)
                        if type3:
                            print 'tpye3'
                            year= string[13:17]
                            day=string[6:8]
                            month=string[9:11]
                            print year,month,day
                        else:
                            year= string[5:9]
                            month=string[10:12]
                            day=string[13:15]
                            print year,month,day
                    #print type(year)
                    
                    today = date.today()

                    
                    try:
                        createday = date(int(year), int(month), int(day))
                    except ValueError,e:
                        return None
                    time_to_createday = abs(createday - today)
                    if time_to_createday.days<366:
                        return 1
                    else:
                        return -1
                else:
                    return None


    #获取真正域名块
    def getrealdomain(self):
            o=urlparse(self.localurl)
            #print o.netloc
            domain='http://whois.chinaz.com/'+o.netloc
            #print domain

            req = Request(domain)
            try:
                response = urlopen(req)
                #print response.geturl()
            except URLError , e :
                if isinstance(e.reason, socket.timeout):
                    print 'socket timeout'
                  
                print "network meets some problems: "
                print "Reason: ",e.reason
                
            else:
                if response!=None:
                    the_page = response.read()
                    #print the_page
                    char = chardet.detect(the_page)
                    #解码为unicode
                    the_page.decode(char['encoding'],'ignore')
                    soup = BeautifulSoup(the_page)
                    #<div class="div_whois">
                    domain=soup.find('div',attrs={"class": "div_relativesearch"})
                    #print type(domain)
                    if domain:
                        text=domain.get_text()
                        tmpdomain= text.split()
                        realdomain=tmpdomain[0]
                        self.domain=realdomain
                
    #指向外域的<emmbed>
    def getlinkembed(self):
            self.getrealdomain()
            linknum=0
            nonelink=0
            outsidelink=0

            for link in self.soup.find_all('embed'):
                    #print(link.get('href'))
                    linknum+=1
                    if link.get('src')==None:
                            nonelink+=1
                    else:
                            o=urlparse(link.get('src'))
                            #print o.netloc
                            if o.netloc:
                                    m=re.search(self.domain,unicode(o.netloc))
                                    if not m:
                                            outsidelink+=1
            #print linknum
            #print nonelink
            #print outsidelink
            value=0.01
            if linknum!=0:
                     value= float(nonelink+outsidelink)/float(linknum)

            if value>=0.2:
                    return 1
            else:
                    return -1
                
                
    #指向外域链接的比例 空域
    def getlink(self):
            self.getrealdomain()
            linknum=0
            nonelink=0
            outsidelink=0

            for link in self.soup.find_all('a'):
                    #print(link.get('href'))
                    linknum+=1
                    if link.get('href')==None:
                            nonelink+=1
                    else:
                            o=urlparse(link.get('href'))
                            #print o.netloc
                            if o.netloc:
                                    m=re.search(self.domain,unicode(o.netloc))
                                    if not m:
                                            outsidelink+=1
            #print linknum
            #print nonelink
            #print outsidelink
            value=0.01
            if linknum!=0:
                    value= float(nonelink+outsidelink)/float(linknum)
            if value>=0.3:
                    return 1
            else:
                    return -1

    #是否有ICP
    def geticp(self):
        #self.getrealdomain()
        #print self.domain
        result=[]
        result= self.soup.find_all(text=re.compile("ICP"))
        if result==[]:
            return 1
        else:
            return -1
        

    #在Search engine中的搜索结果  baidu
    def getsearchengine(self):
        #http://www.baidu.com/s?wd=51ylc.com&ie=UTF-8
            self.getrealdomain()
            query='http://www.baidu.com/s?wd='+self.domain+'&ie=UTF-8'
            print query

            req = Request(query)
            try:
                response = urlopen(req)
                #print response.geturl()
            except URLError , e :
                if isinstance(e.reason, socket.timeout):
                    print 'socket timeout'
                  
                print "network meets some problems: "
                print "Reason: ",e.reason
                
            else:
                if response!=None:
                    the_page = response.read()
                    #print the_page
                    char = chardet.detect(the_page)
                    #解码为unicode
                    the_page.decode(char['encoding'],'ignore')
                    soup = BeautifulSoup(the_page)
                    for link in soup.find_all('span',attrs={"class":'g'}):
                    #print type(link)
                        m=re.search(self.domain,link.get_text().split()[0])
                        if m:
                            return -1

            return 1




    # keywords域
    #print soup.find_all("meta",attrs={"name": "keywords"})
    # description域
    # print soup.find_all("meta",attrs={"name": "description"})
    
    
    
    
    #获取域名相关
    
    '''
     <div id="whoisinfo" class="div_whois">
        注册商：GODADDY.COM, LLC<br/>
        域名服务器：whois.godaddy.com<br/>
        DNS服务器：DNS1.FREEHOSTIA.COM<br/>
        DNS服务器：DNS2.FREEHOSTIA.COM<br/>
        域名状态：运营商设置了客户禁止删除保护<br/>
        域名状态：运营商设置了客户禁止续费保护<br/>
        域名状态：运营商设置了客户禁止转移保护<br/>
        域名状态：运营商设置了客户禁止修改保护<br/>
        更新时间：2012年05月28日<br/>
        创建时间：2012年05月23日<br/>
        过期时间：2013年05月23日<br/>
        联系人：zhu, alice<br/>
        联系方式：<img src="/displayemail.aspx?email=M8N8oc1O|iQhqGCDHdpH9m77v2qrQfW8"/>
        <br/>
        <br/>
    </div>
     '''

        
 
    #返回提取到的内容向量 列表结构
        
    #[标题，页面关键字提取，页面链接文字比，
    #  页面的ICP声明部分，页面是否含有明显的form域，页面对应的域名信息（多个字段） ]
    def getvector(self):
        result=[]
        getip=self.geturlip()
        result.append(self.getport())
        result.append(getip)
        #result.append(self.geturlat())
        result.append(self.geturldot())
        if getip==1:
            result.append(1)
        else:
            result.append(self.getdomainage())
        
        if self.soup:
            
            
            result.append(self.geticp())
            result.append(self.getlink())
            result.append(self.getlinkembed())
            if getip==1:
                result.append(1)
            else:
                result.append(self.getsearchengine())
            
           
        return result
        


if __name__ == "__main__":
       
    url=['http://www.baidu.com','https://www.baidu.com',
         'http://www.12306.cn/mormhweb/','https://www.alipay.com/',
         'https://kyfw.12306.cn/otn/lcxxcx/init','tkda;fkaa;skf','http://www.kdfasjdklfasl.com','http://bbs.chinaunix.net/forum-141-1.html',
         'www.baidu.com','http://www.dmoz.org/World/Chinese_Simplified/商业/电子商务/支付系统/',
         'http://192.33.33.33:8080/@jdkfs/142.33.33.33/kdfj;af','http://172.31.159.57/钓鱼分类/娱乐/中国梦想秀/bpseruz/main.html']
    #url=['http://172.31.159.57/钓鱼分类/娱乐/中国梦想秀/bpseruz/main.html','https://mail.qq.com/cgi-bin/loginpage']

    #url=['http://172.31.159.57/钓鱼分类/企业/Apple/lost-apple/main.html','http://mail-lost-apple.com/cgi-bin/WebObjects/MyAppleId.woa/wa/submited?token=6894a7d8-1c4e-4b96']

    test=chavector(url[0])
    vector=test.getvector()
    print vector
    '''
    for strulr in url:
        test=chavector(strulr)
        vector=test.getvector()
        if len(vector)==8:
            print vector
        else:
            print 'error'
        print '----------------------------------------------'

    '''
