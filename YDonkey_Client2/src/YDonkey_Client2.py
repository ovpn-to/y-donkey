
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
ed.hello(("localhost",10001))