
__author__="qianjin"
__date__ ="$2009-3-17 16:18:23$"

if __name__ == "__main__":
    print "Hello";

import time

f4 = open("2009-03-08-taobao-access_log")

start = time.clock()
for line in f4:
#    print line
    pass
end = time.clock()
print end - start

f3 = open("2009-03-08-taobao-access_log")
start = time.clock()
while 1:
    lines = f3.readlines(1000000)
    if not lines:break
    for line in lines:
        pass
end = time.clock()
print end - start


import fileinput
start = time.clock()
for line in fileinput.input("2009-03-08-taobao-access_log"):
    pass
end = time.clock()
print end - start

f1 = open("2009-03-08-taobao-access_log")
start = time.clock()
while 1:
    line = f1.readline()
    if not line:break
    pass
end = time.clock()
print end - start