#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from chavector import *
import os
'''
参数全是字符串
'''





parser = argparse.ArgumentParser()
parser.add_argument("urlfile",help="the first argument is filepath")
parser.add_argument("task",help="the second argument is taskname")
args = parser.parse_args()


if os.path.exists(args.urlfile):
    print 'start vector get'
    record=[]
    weight=[]
    dictdata=dict()
    value=0.0
    with open('trainresult.txt', 'r') as f:
        read_data = f.readlines()
    for data in read_data:
        temp=data.strip().split()
        weight.append(map(float,temp))
    #print weight[0][0]
    
    with open(args.urlfile, 'r') as f:
        read_data = f.readlines()

    for data in read_data:
        data2=data.strip()
            #print data2
        if data2:
            #print data.decode('utf-8')
            splitdata=data2.split()
            if len(splitdata)==1:
                test=chavector(splitdata[0])
                vector=test.getvector()
                if len(vector)==8:
                    value=weight[0][0]*vector[0]+weight[0][1]*vector[1]+weight[0][2]*vector[2]+weight[0][3]*vector[3]+weight[0][4]*vector[4]+weight[0][5]*vector[5]+weight[0][6]*vector[6]+weight[0][7]*vector[7]
                    print value
                    dictdata[splitdata[0]]=value
    print dictdata

    with open(args.task, 'w') as f:
        for k,v in dictdata.iteritems():
            tmp=k+' '+str(v)
            f.write(tmp)
            f.write('\n')
    print 'end vector get'
else:
    print 'the file path is error'
