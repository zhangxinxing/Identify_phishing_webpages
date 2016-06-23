#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from compute import *
import os
'''
参数全是字符串
'''





parser = argparse.ArgumentParser()
parser.add_argument("urlfile",help="the first argument is filepath")
args = parser.parse_args()


if os.path.exists(args.urlfile):
    print 'start train'
    train=compute(args.urlfile)
    train.getvectors()
    train.getrates()
    print 'end train'
else:
    print 'the file path is error'
