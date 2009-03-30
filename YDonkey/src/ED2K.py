##!/usr/bin/env python
## coding:utf-8 ##
#### ED2K Lib ####

import struct
import os
import hashlib

from ED2K_BASE import *

__author__ = "qianjin"
__date__ = "$2009-2-26 10:26:58$"
__all__ = ["Ed2kServer","Ed2kClient","Ed2k"]


class Ed2kServer(Ed2k):
    """
    Ed2kServer
    """
    
    def __init__ (self, host='', port=SPORT):
        Ed2k.__init__(self,host,port)        

    ""
    def op_ServerMessage(self,msg):
        fmt = "!BH%ds" % len(msg)
        li = [OP_SERVERMESSAGE,len(msg),msg]
        li.append(fmt)
        return li
    ""
    def op_ServerStatus(self):
        fmt = "!BII"
        li = [OP_SERVERSTATUS,self.cnt_users,self.cnt_files]
        li.append(fmt)
        return li
    ""
    def op_IDChange(self,newid):
        fmt = "!BI"
        li = [OP_IDCHANGE,newid]
        li.append(fmt)
        return li
    ""
    def op_ServerList(self):
        pass
    ""
    def op_ServerIdent(self):
        fmt = "!B16s4sHI"
        li = [OP_SERVERIDENT]
#        print self.GUID
        li.append(self.GUID)
        li.append(socket.inet_aton(socket.gethostbyname(self.host)))
        li.append(self.port)
        li.append(2)

        buf = self.ct_SERVERNAME(self.server_name)
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_SERVERDESC(self.server_desc)
        fmt += buf[0]
        li.extend(buf[1:])

        li.append(fmt)
#        print li
#        return apply(struct.pack,(fmt,) + tuple(li))
        return li
    def op_SearchResult(self,files):
        fmt = "!BI"
        li = [OP_SEARCHRESULT,len(files)]
        
        for file in files:
#            print self.filelist[file]
            fmt += "16s4sHI"
            li.append(self.filelist[file]["hash"])
            li.append(self.filelist[file]["ip"])
            li.append(self.filelist[file]["port"])
            li.append(5)

            buf = self.ct_FILENAME(self.filelist[file]["name"])
            fmt += buf[0]
            li.extend(buf[1:])

            buf = self.ct_FILESIZE(self.filelist[file]["size"])
            fmt += buf[0]
            li.extend(buf[1:])

            buf = self.ct_FILETYPE(self.filelist[file]["type"])
            fmt += buf[0]
            li.extend(buf[1:])

            buf = self.ct_SOURCES(self.filelist[file]["src"])
            fmt += buf[0]
            li.extend(buf[1:])

            buf = self.ct_COMPLSRC(self.filelist[file]["complsrc"])
            fmt += buf[0]
            li.extend(buf[1:])

        li.append(fmt)
#        print li
#        return apply(struct.pack,(fmt,) + tuple(li))
        return li



class Ed2kClient(Ed2k):
    def __init__ (self, host = '', port = None):
        if not port:
            port = random.randint(10000,15000)
        Ed2k.__init__(self,host,port)

    def login(self,addr):

        th = threading.Thread(target=self.__login,
            args=[addr])
        th.setName("Thread<login>")
        th.start()
#        t_login.join()
    def __login(self,addr):
        print "%s login!" % threading.currentThread().getName()

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(addr)
        except socket.error, e:
            print "can not connect"
            sys.exit(1)
        self.sock = sock
        print "connected %s" % repr(addr)
        buf = self.pack_ED2K(self.op_LoginRequset())
        sock.send(buf)
#        print "send ok"
        while 1:
            try:
#                sleep(10)
                buf = sock.recv(1024)
#                print "recv %s" %repr(buf)
#                print "recv: %s" % repr(buf)
                self.parser(sock,buf,len(buf))
#                self.updateServerInfo(sock)
#                self.offerFile(sock)
#                self.search(sock,"searchexpr")
            except socket.error, e:
                self.error(e, "linkage interrupt")
            


    def updateServerInfo(self):
        self.__updateServerInfo(self.sock)
        
    def __updateServerInfo(self,sock):
        sock.send(self.pack_ED2K(self.op_GetServerList()))


    def __initFileTable(self):
        ShareFolder = "d:\download\\"
        for root,dirs,files in os.walk(ShareFolder):
            for file in files:
                finfo = self.path2file(ShareFolder,file)
                self.filelist[finfo["hash"]] = finfo

        pass

    def path2file(self,folder,file):
        md4 = hashlib.new("md4")
        fd = open(folder+file)
        data = fd.read()
        md4.update(data)
        hash = md4.digest()
        info = {"hash":hash,"name":file,"size":len(data),"type":"TXT","src":1,"complsrc":1}
        fd.close()
        return info

    def offerFile(self):
        self.__offerFile(self.sock)
    def __offerFile(self,sock):
        """
        DONE:将offerfile改成多多文件同发的
        """
        self.__initFileTable()
        sock.send(self.pack_ED2K(self.op_OfferFiles(self.filelist)))

    def search(self,expr):
        self.__search(self.sock,expr)
    def __search(self,sock,expr):
        sock.send(self.pack_ED2K(self.op_Search(expr)))

    def download(self,file):
        pass
        
        
    """
    OP Codes Packs
    """
    
    def op_LoginRequset(self):
        fmt = "!B16s4sHI"
        li = [OP_LOGINREQUEST]
        li.append(self.GUID)
        li.append(socket.inet_aton(socket.gethostbyname(self.host)))
        li.append(self.port)
        li.append(5)

        buf = self.ct_NICK("YH_SCU")
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_VERSION()
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_PORT(self.port)
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_MULEVERSION(1234)
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_FLAGS(0)
        fmt += buf[0]
        li.extend(buf[1:])

        li.append(fmt)
#        print li
#        return apply(struct.pack,(fmt,) + tuple(li))
        return li

    ""
    def op_GetServerList(self):
        fmt = "!B"
        li = [OP_GETSERVERLIST]
        li.append(fmt)
        return li


    def op_OfferFiles(self,filelist):
        fmt = "!BI"
        li = [OP_OFFERFILES,len(filelist)]
        for file in filelist:
#            print repr(filelist[file])
            fmt +="16s4sHI"
            li.append(filelist[file]["hash"])
            li.append(socket.inet_aton(socket.gethostbyname(self.host)))
            li.append(self.port)
            li.append(3)
            buf = self.ct_FILENAME(filelist[file]["name"])
            fmt += buf[0]
            li.extend(buf[1:])
            buf = self.ct_FILESIZE(filelist[file]["size"])
            fmt += buf[0]
            li.extend(buf[1:])
            buf = self.ct_FILETYPE(filelist[file]["type"])
            fmt += buf[0]
            li.extend(buf[1:])

        li.append(fmt)
#        print li
        return li

    def op_Search(self,expr):
        fmt = "!BH%ds" % len(expr)
        li = [OP_SEARCH,len(expr),expr]

        li.append(fmt)
#        print li
#        return apply(struct.pack,(fmt,) + tuple(li))
        return li


    """
    client to client
    """
    def op_Hello(self):
        fmt = "!B16s4sHI"
        li = [OP_HELLO]
        li.append(self.GUID)
        li.append(socket.inet_aton(socket.gethostbyname(self.host)))
        li.append(self.port)
        li.append(5)

        buf = self.ct_NICK("YH_SCU")
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_VERSION()
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_PORT(self.port)
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_MULEVERSION(1234)
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_FLAGS(0)
        fmt += buf[0]
        li.extend(buf[1:])

        li.append(fmt)
#        print li
#        return apply(struct.pack,(fmt,) + tuple(li))
        return li
        pass
    def op_ReqFile(self,hash):
        fmt = "!B16H"
        li = [OP_REQFILE]
        li.extend(hash)
        li.append(fmt)
        return li
    def op_SetReqFileID(self,hash):
        fmt = "!B16H"
        li = [OP_SETREQFILEID]
        li.extend(hash)
        li.append(fmt)
        return li
    def op_ReqHashSet(self,hash):
        fmt = "!B16H"
        li = [OP_REQHASHSET]
        li.extend(hash)
        li.append(fmt)
        return li
    def op_StartUploadReq(self,hash):
        fmt = "!B16H"
        li = [OP_STARTUPLOADREQ,hash]
        li.append(fmt)
        return li
    def op_ReqChunks(self,hash,begin,end):
        fmt = "!B16H"
        li = [OP_REQCHUNKS,hash]
        fmt += "6I"
        li.extend(begin)
        li.extend(end)
        li.append(fmt)
        return li

    def op_FileName(self,hash,name):
        fmt = "!B16HI%ds" % len(name)
        li = [OP_FILENAME,hash,len(name),name]
        li.append(fmt)
        return li
    def op_FileDesc(self,rating,comment):
        fmt = "!BHI%ds" % len(comment)
        li = [OP_FILEDESC,rating,len(comment),comment]
        li.append(fmt)
        return li
    def op_ReqFile_Status(self,hash,partmap):
        pass
    def op_ReqFile_NoFile(self,hash):
        fmt = "!B16H"
        li = [OP_REQFILE_NOFILE,hash]
        li.append(fmt)
        return li
    def op_HashSet(self,hash,parts):
        fmt = "!B16HH"
        li = [OP_HASHSET,hash,len(parts)]
        for i in parts:
            fmt += "16H"
            li.append(i)
        li.append(fmt)
        return li
    def op_AcceptUploadReq(self):
        fmt = "!B"
        li = [OP_ACCEPTUPLOADREQ]
        li.append(fmt)
        return li

    def op_QueueRanking(self,rank):
        fmt = "!BI"
        li = [OP_ACCEPTUPLOADREQ,rank]
        li.append(fmt)
        return li
    def op_SendingChunk(self,hash,begin,end,data):
        fmt = "!B16HII%ds" % len(data)
        li = [OP_SENDINGCHUNK,hash,begin,end,data]
        li.append(fmt)
        return li
    def op_CancelTransfer(self):
        fmt = "!B"
        li = [OP_CANCELTRANSFER]
        li.append(fmt)
        return li