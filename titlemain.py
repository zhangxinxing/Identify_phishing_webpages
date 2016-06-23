import argparse
from classtitle import *
import os
'''
参数全是字符串
'''





parser = argparse.ArgumentParser()
parser.add_argument("whitefile",help="the first argument is filepath")
parser.add_argument("blackfile",help="the second argument is filepath")
parser.add_argument("filename",help="the third argument is filename")
args = parser.parse_args()


if os.path.exists(args.whitefile) and os.path.exists(args.blackfile):
    print 'start title compare'
    ofile=classtitle(args.whitefile,args.blackfile)
    ofile.writefile(args.filename)
    print 'end title compare'
else:
    print 'the file path is error'


