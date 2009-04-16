#!/usr/bin/python
__author__="qianjin"
__date__ ="$2009-3-30 13:46:00$"

if __name__ == "__main__":
    print "Hello";



import threading
from time import *
import ED2K
from ED2K_BASE import *






ed = ED2K.Ed2kClient(port=10002)
ed.listen()
sleep(1)
ed.login(("localhost", SPORT))
sleep(1)
ed.updateServerInfo()
sleep(1)
ed.search(".*10.*")

ed.download((socket.gethostbyname("localhost"),10001),binascii.a2b_hex("02CFFFD6DA9DEFE30A958BE970747143"))
#ed.hello(("localhost",10001))

