
__author__="qianjin"
__date__ ="$2009-3-27 10:49:20$"

if __name__ == "__main__":
    print "Hello";


import re


s = re.search('.*abc*', '1212abcsdasda')
print s.group()
m = re.match('.*abc.*', 'fsdfsdfsdf')
if m :
    print m.group()