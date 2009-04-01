#! /usr/bin/python
## coding:utf-8 ##
"""
Ed2kClient Test
"""
if __name__ == "__main__":
    print "Main Ed2kClient Test";

import threading
from time import *
import ED2K
from ED2K_BASE import *




    

ed = ED2K.Ed2kClient(port=10001)
ed.listen()
sleep(1)
ed.login(("localhost", SPORT))
sleep(1)
ed.updateServerInfo()
#
ed.offerFile()








