##!/usr/bin/env python
## coding:utf-8 ##
####  π”√Socket,Selectø‚ ####

from socket import *
import select

host = ''
port = 9999

s = socket(AF_INET, SOCK_STREAM)
s.bind((host,port))
s.listen(5)
#print "ip : ",s.getpeername()
addr = gethostbyname("localhost")
print type(addr)
print type(inet_aton(addr))
print len(inet_aton(addr))
print repr(inet_aton(addr))
while 1:
    infds,outfds,errfds = select.select( [s, ],[],[],5)
    if len(infds) != 0:
        clientsock,clientaddr = s.accept()
        buf = clientsock.recv(8196)
        if len(buf) != 0:
                print (buf)
        clientsock.close()

    print "no data coming"