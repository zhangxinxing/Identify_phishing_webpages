import argparse
from classfile import *
import os
import re
'''
参数全是字符串
白名单的添加 -add whitetype urlfile
白名单的合并 -merge path1 path2
白名单的删除 -del path timestr


[\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d]
'''





parser = argparse.ArgumentParser()
parser.add_argument("argumentone",help="the first argument is filepath")
parser.add_argument("argumenttwo",help="the second argument is filepath or time string")
parser.add_argument("-a", "--add",action="store_true",help="add the whiteurl,the argumentone is the typewhite,the argumenttwo is url file")
parser.add_argument("-m", "--merge",action="store_true",help="merge the whiteurl,")
parser.add_argument("-d", "--delete",action="store_true",help="delete the whiteurl by time string the format is like \"[2015-02-21 19:33:34]\" ")

args = parser.parse_args()


if args.add:
    print "add"
    if os.path.exists(args.argumentone) and os.path.exists(args.argumenttwo):
        print 'start add new white url'
        ofile=classfile()
        ofile.addfile(args.argumentone,args.argumenttwo)
    else:
        print 'the file path is error'
elif args.merge:
    print "merge"
    if os.path.exists(args.argumentone) and os.path.exists(args.argumenttwo):
        print 'start the merge'
        ofile=classfile()
        ofile.mergefile(args.argumentone,args.argumenttwo)
    else:
        print 'the file path is error'
elif args.delete:
    if not os.path.exists(args.argumentone):
        print 'the file path is error' 
    elif not re.match(r'\[\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d\]',args.argumenttwo):
        print 'timestr is not right'
    else:
        print 'delete start'
        ofile=classfile()
        ofile.delfile(args.argumentone,args.argumenttwo)
else:
    print "less option"
