#! /usr/bin/python

__author__="qianjin"
__date__ ="$2009-2-27 9:58:17$"

if __name__ == "__main__":
    print "Threading";


import threading
import time

def childthread(str = "", nint = 0):
    cnt = 0
    while cnt != 30:
        print "%s, %d\n" % (threading.currentThread().getName(),cnt)
        print "str = %s , nint = %d" % (str,nint)
        time.sleep(1)
        cnt += 1




while 1:
    t = threading.Thread(target = childthread,
                        args = ["hello",5473])
    t.setDaemon(True)
    t.start()
    print "%s, %s\n" % (threading.currentThread().getName(),time.ctime())
    #t.join()
    time.sleep(5)


