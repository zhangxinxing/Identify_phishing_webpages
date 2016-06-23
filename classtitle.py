#!/usr/bin/python
# -*- coding: utf-8 -*-

import jieba
from urllib2 import Request, urlopen, URLError, HTTPError
from bs4 import BeautifulSoup

from datetime import datetime

import chardet

import socket
socket.setdefaulttimeout(30) 

class classtitle():

    def __init__(self,fileone,urlfile):
        #初始化白名单标题数据
        dictdata=dict()

        with open(fileone, 'r') as f:
            read_data = f.readlines()

        for data in read_data:
            data2=data.strip()
            #print data2
            if data2:
            #print data.decode('utf-8')
                splitdata=data2.split()
                #record=[splitdata[0]+' '+splitdata[1],splitdata[2],splitdata[3],splitdata[4]]
                dictdata[splitdata[3]]=splitdata[4]

        #print dictdata
        self.white=dictdata

        #初始化黑名单标题数据
        dictdata2=dict()
        record=[]
        with open(urlfile,'r') as f:
                urls = f.readlines()
                
        i=0
        for url in urls:
            data=url.strip()
            if data:
                #print data
                result=self.gettitle(data)
                #print result
                if result!=None and result!=[] and result[1]!='':
                    dictdata2[data]=result[1]
        #print dictdata2
        self.black=dictdata2
        
        
    #获取标题
    def gettitle(self,url):
        result=[]
        req = Request(url)
        try:
            response = urlopen(req)
        except URLError , e :
            if isinstance(e.reason, socket.timeout):
               return None
            print "network meets some bad things: "
            print "Reason: ",e.reason
            return None
        else:
            if response!=None:
                    
                    the_page = response.read()
                    char = chardet.detect(the_page)
                    #print char
                    the_page.decode(char['encoding'],'ignore').encode('utf-8','ignore')
                    realurl=''
                    realurl  = response.geturl().decode('utf-8','ignore')
                    soup = BeautifulSoup(the_page)
                    # print unicode(soup.title.string)
                    title=''
                    if soup.title!=None:
                        title=soup.title.string
                    # 解码为utf-8
                    result.append(realurl.encode('utf-8','ignore'))
                    result.append(title.encode('utf-8','ignore'))
        finally:
            print 'gettitle success ----',url
            if len(result)==2:
                return result
            else:
                return None

    #比较标题，返回相似度
    def comparestr(self,str1,str2):
        #str3="奔跑吧！兄弟"
        #str4="奔跑兄弟！奔跑吧年少 设计开发时间 手机费"
        str5=str1.decode('utf-8','ignore').strip()
        str6=str2.decode('utf-8','ignore').strip()

        #100% 比较
        data=[]
        data2=[]

        data.append(str5)
        data2.append(str6)
        if data==data2:
            print '100 same ....'
        else:
            #分词比较
            wordlist=list(jieba.cut(str5))
            blanknum=wordlist.count(' ')
            while blanknum>0:
                wordlist.remove(' ')
                blanknum-=1
            print 'title 1'
            print wordlist


            wordlist2=list(jieba.cut(str6))
            blanknum=wordlist2.count(' ')
            while blanknum>0:
                wordlist2.remove(' ')
                blanknum-=1
            print 'title 2'
            print wordlist2

            for word in wordlist:
                print word.encode('utf-8')
            #折中  你好 -- 你好你好   按字符的比较   不同 去重
            #设q是字符串1和字符串2中都存在的单词的总数，
            #s#是字符串1中存在，字符串2中不存在的单词总数，
            #r是字符串2中存在，字符串1中不存在的单词总数，
            #t是字符串1和字符串2中都不存在的单词总数。
            #我们称 q,r,s,t为字符串比较中的4个状态分量。如图1所示：
            #相似度=q/(q+r+s) 公式1

            set1=set(wordlist)
            set2=set(wordlist2)

            #q
            q=0
            for word in set1:
                if word in set2:
                    q+=1
            #print '--------'
            #print q

            #r
            r=0
            for word in set2:
                if word not in set1:
                    r+=1
            #print '--------'
            #print r

            #s
            s=0
            for word in set1:
                if word not in set2:
                    s+=1
            #print '--------'
            #print s

            q=float(q)
            r=float(r)
            s=float(s)

            VALUE1=float(q/(q+r+s))*100

            #return VALUE1

        #奔跑吧！兄弟 -- 兄弟！奔跑吧  按字符加位置的比较 对称 状态分布量  同义词

            len1=len(wordlist)
            len2=len(wordlist2)
            minlen=min(len1,len2)
            maxlen=max(len1,len2)
            if minlen==len1:
                set1=wordlist
                set2=wordlist2
            else:
                set2=wordlist
                set1=wordlist2

            #q samenum
            q=0
            k=minlen-1
            while k>0:
                if set1[k] == set2[k]:
                    q+=1
                k-=1
            #print '--------'
            #print 'wenzhi:',q

            q=float(q)
            r=float(maxlen)

            VALUE2=float(q/r)*100
            #print VALUE2
            TOTAL=VALUE2*0.4+VALUE1*0.6
            print 'total:' ,TOTAL
            return TOTAL

    #目前将相似度大于60%的数据写入文件   【time，blackurl,blacktitle,wurl,wtitle,value]
    def writefile(self,filename):
        record=[]
        for (k,v) in  self.white.items():
            
            #print "dict[%s]=" % k,v
            for (k2,v2) in  self.black.items():
                value=self.comparestr(v,v2)
                if  value>0:
                    #print "dict[%s]=" % k,v ,k2,v2,value
                    tmplist=[]
                    tmplist.append('['+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+']')
                    tmplist.append(k)
                    tmplist.append(v)
                    tmplist.append(k2)
                    tmplist.append(v2)
                    tmplist.append(str(value))
                    #print tmplist
                    delimiter = ' '
                    record.append(delimiter.join(tmplist))
                #print unicode(data).decode('utf-8')
            #print record
                    
        if record!=[]:
            with open(filename,'a+') as f:
                for lines in record:
                    f.write(lines)
                    f.write('\n')
        
