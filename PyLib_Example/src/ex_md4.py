
__author__="qianjin"
__date__ ="$2009-3-2 19:06:21$"

if __name__ == "__main__":
    print "Hello";

import hashlib
#passwd = 'hello'
#print hashlib.new('md4').hexdigest().upper()

md4 = hashlib.new("md4")

f = open("1.pdf","rb")
while 1:
    date = f.read(9280000)
    if not date:break
    md4.update(date)
f.close
#print date


#md4.update("hello")
095d3989c42f1b124fa59cee5d206d4a


print md4.block_size
print md4.digest_size
print repr(md4.digest())
print md4.hexdigest()

