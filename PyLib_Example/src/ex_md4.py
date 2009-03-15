
__author__="qianjin"
__date__ ="$2009-3-2 19:06:21$"

if __name__ == "__main__":
    print "Hello";

import hashlib
passwd = 'mygreatpasswd'
print hashlib.new('md4', passwd.encode('utf-16le')).hexdigest().upper()


