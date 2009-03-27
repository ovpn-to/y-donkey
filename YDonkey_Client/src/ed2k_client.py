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




    

ed = ED2K.Ed2kClient()
ed.listen()
sleep(1)
ed.login(("localhost", SPORT))
sleep(1)
ed.updateServerInfo()

ed.offerFile()
ed.offerFile()

ed.search(".*1.*")

#t_listen = threading.Thread(target = ed.listen);
#t_listen.setDaemon(True)
#t_listen.start()

#print repr(ed.op_LoginRequset("goof"))


#while 1:
#    t_login = threading.Thread(target=ed.login,
#            #args=[("no1.eserver.emule.org.cn",8080)])
#            #args=[("193.42.213.70",6000)])
#            args=[("localhost", SPORT)])
#    t_login.start()
#    t_login.join()

#ed.login(("localhost",SPORT))
#ed.updateServerInfo(ed.sock)



