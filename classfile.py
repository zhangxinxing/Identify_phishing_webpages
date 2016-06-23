#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
Created on 2015-02-22 ---  2015-02-25

@author: zhang&*&*&

'''


'''
__init__: pass

mergefile:参数传递 合拼的两个文件 同格式 
参数fileone filetwo 为文件打开路径


mergefile:参数传递 合拼的两个文件 同格式 
参数fileone filetwo 为文件路径
        两个白名单文件的合并 相同格式
        分别读取
        以字典为存储结构 并以url为关键字去重
        去重后，以时间为序，按序排列
        并合并到第一个文件中



addfile:参数传递
将urlfile文件中的url提取标题后 写入到infile 并有去重功能

参数infine urlfile均为文件路径

读取urlfile文件中的url
调用gettitle()获取页面标题，当url无法正常获取标题时，将被自动略去
 生成tmp文件后，调用mergefile合并

gettitle:url

获取给定url的标题 返回标题以utf编码 以及真正的返回url
当url获取的标题有问题是，将返回None

delfile:  删除给定日期之前的白名单数据数据
delfile 需要做切割的文件路径
timestr 时间串
#delfile('1.txt','[2015-02-21 19:33:34]')

删除某一时间之前的数据

'''

from urllib2 import Request, urlopen, URLError, HTTPError
from bs4 import BeautifulSoup

from datetime import datetime

import chardet

import socket
socket.setdefaulttimeout(30) 

class classfile:

    def __init__(self):
        pass
        

    def mergefile(self,fileone,filetwo):

        dictdata=dict()

        with open(fileone, 'r') as f:
            read_data = f.readlines()

        for data in read_data:
            data2=data.strip()
            if data2:
            #print data.decode('utf-8')
                splitdata=data2.split()
                record=[splitdata[0]+' '+splitdata[1],splitdata[2],splitdata[3],splitdata[4]]
                dictdata[record[2]]=[record[0],record[3]]
            
        with open(filetwo, 'r') as f:
            read_data = f.readlines()

        for data in read_data:
            data2=data.strip()
            if data2:
            #print data2.decode('utf-8')
                splitdata=data2.split()
                record=[splitdata[0]+' '+splitdata[1],splitdata[2],splitdata[3],splitdata[4]]
                dictdata[record[2]]=[record[0],record[3]]
            

        unicode(dictdata)
        #排序
        sortedrecord=sorted(dictdata.iteritems(), key=lambda d:d[1], reverse = False )

        unicode(sortedrecord)

        with open(fileone, 'w') as f:
            i=0
            record=[]
            for data in sortedrecord:
                i=i+1
                tmp=[]
                tmp.append(data[1][0])
                tmp.append(str(i))
                tmp.append(data[0])
                tmp.append(data[1][1])
                delimiter = ' '
                record.append(delimiter.join(tmp))
                #print unicode(data).decode('utf-8')
            #print record
            for lines in record:
                f.write(lines)
                f.write('\n')
                
        print 'merge success -->>', fileone



    def addfile(self,infile,urlfile):
        record=[]
        with open(urlfile,'r') as f:
                urls = f.readlines()
                
        i=0
        for url in urls:
            data=url.strip()
            if data:
                #print data
                result=self.gettitle(data)
                if result!=None and result!=[] and result[1]!='':
                    i+=1
                   # print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    tmplist=[]
                    tmplist.append('['+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+']')
                    tmplist.append(str(i))
                    tmplist.append(result[0])
                    tmplist.append(result[1])
                    #print tmplist
                    delimiter = ' '
                    record.append(delimiter.join(tmplist))
                #print unicode(data).decode('utf-8')
            #print record
                    
        if record!=[]:
            with open('tmp','w') as f:
                for lines in record:
                    f.write(lines)
                    f.write('\n')
        self.mergefile(infile,'tmp')
        print 'new url is added ---- >',infile

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
                    realurl  = response.geturl().decode('utf-8','ignore')
                    soup = BeautifulSoup(the_page)
                    # print unicode(soup.title.string)
                    title=''
                    if soup.title!=None:
                        title=soup.title.string.strip().replace(' ','')
                    # 解码为utf-8
                    result.append(realurl.encode('utf-8','ignore'))
                    result.append(title.encode('utf-8','ignore'))
        finally:
            print 'gettitle success ----',url
            if len(result)==2:
                return result
            else:
                return None

    def delfile(self,delfile,timestr):
        with open(delfile, 'r') as f:
            read_data = f.readlines()
        #print read_data
        delnum=0
        for data in read_data:
            data2=data.strip()
            if data2:
                splitdata=data2.split()
                #print splitdata
                record=[splitdata[0]+' '+splitdata[1]]
                if record[0]>=timestr:
                    delnum=int(splitdata[2])-1
                    break
        if delnum>0:
            del read_data[0:delnum]
            with open(delfile, 'w') as f:
                f.writelines(read_data)
        self.mergefile(delfile,'blank')
        print 'delfile success-----',delfile
        
