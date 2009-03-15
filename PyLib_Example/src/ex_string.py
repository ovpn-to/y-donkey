
__author__="qianjin"
__date__ ="$2009-3-2 19:57:06$"

if __name__ == "__main__":
    print "Hello";
import struct

str = '\x01fuck\x01\x00\x0cloginrequest'

print struct.unpack("!B4s", str[0:5])


