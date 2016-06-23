#!/usr/bin/python
# -*- coding: utf-8 -*-

from chavectortrain import *


class compute:

    def __init__(self,filepath):
        self.filepath=filepath


    def getvectors(self):
        #计算矩阵
        record=[]
        with open(self.filepath, 'r') as f:
            read_data = f.readlines()

        for data in read_data:
            data2=data.strip()
            #print data2
            if data2:
            #print data.decode('utf-8')
                splitdata=data2.split()
                if len(splitdata)==3:
                    test=chavector(splitdata[0],splitdata[1])
                    print 'local url ',splitdata[0]
                    print 'real url',splitdata[1]
                    vector=test.getvector()
                    if len(vector)==8:
                        vector.append(splitdata[2])
                        record.append(vector)

                        
        with open("traintmp",'w') as f:
            for lines in record:
                f.write(str(lines))
                f.write('\n')
    #计算权值
    def getrates(self):
        ee=[]
        ff=[]#false
        ft=[]#true
        ww=[]
        record=[]
        result=[]
        new=''
        with open("traintmp", 'r') as f:
            read_data = f.readlines()
        for data in read_data:
            for ch in data:
                if ch not in ['[',']',',','\'','\n']:
                    new+=ch
            
            record.append(new)
            new=''
        #print record
        for data in record:
            temp=data.strip().split()
            #print temp
            if len(temp)==9:
                if 'None' not in temp:
                    result.append(map(float,temp))
        #print result
        #ok
        size=len(result)
        print size
        for i in range(0,8):
            tmpff=0
            tmpft=0
            tmpee=0
            for j in range(0,size):
                if result[j][i]==result[j][8]:
                    tmpft+=1
                else:
                    tmpff+=1
            print tmpft,tmpff
            tmpee=float(tmpft-tmpff)/float(size)
            ff.append(tmpff)
            ft.append(tmpft)
            ee.append(tmpee)
        print ee
        eesum=0
        for i in range(0,8):
            eesum+=ee[i]
        for i in range(0,8):
            ww.append(ee[i]/eesum)
        print ww
        with open("trainresult",'w') as f:
                for data in ww:
                    f.write(str(data))
                    f.write(' ')
if __name__ == "__main__":
    train=compute("train52.txt")
    train.getvectors()
    train.getrates()

