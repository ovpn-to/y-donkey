## coding=utf-8 ##
__author__="qianjin"
__date__ ="$2009-2-27 14:35:39$"

if __name__ == "__main__":
    print "Hello";

from time import ctime,sleep,time
import select
import socket
import threading
import ctypes
import random
import struct
import sys
from struct import unpack
import re


#Protocol Code
PR_ED2K = 0xe3
PR_EMULE = 0xc5
PR_ZLIB = 0xd4

#OP Code
OP_LOGINREQUEST = 0x01
OP_SERVERMESSAGE= 0x38
OP_SERVERSTATUS = 0x34
OP_IDCHANGE     = 0x40
OP_GETSERVERLIST= 0x14
OP_SERVERLIST   = 0x32
OP_SERVERIDENT  = 0x41
OP_OFFERFILES   = 0x15
OP_SEARCH       = 0x16
OP_SEARCHRESULT = 0x33
OP_HELLO        = 0x03  #原为0x01
OP_HELLOANSWER  = 0x4C
OP_REQFILE      = 0x58
OP_FILENAME     = 0x59
OP_FILEDESC     = 0x61
OP_REQFILE_STATUS   = 0x50
OP_REQFILE_NOFILE   = 0x48
OP_REQHASHSET   = 0x51
OP_HASHSET      = 0x52
OP_STARTUPLOADREQ   = 0x54
OP_ACCEPTUPLOADREQ  = 0x5c
OP_QUEUERANKING     = 0x5c
OP_REQCHUNKS    = 0x47
OP_SENDINGCHUNK = 0x46
OP_CANCELTRANSFER   = 0x56
OP_SETREQFILEID = 0x4f



#Tags
CT_NICK         = 0x01
CT_VERSION      = 0x11
CT_PORT         = 0x0f
CT_MULEVERSION  = 0xfb
CT_FLAGS        = 0x20
CT_SERVERNAME   = 0x02  #协议有冲突 原为0x01
CT_SERVERDESC   = 0x0b
CT_FILENAME     = 0x31  #原为0x01
CT_FILESIZE     = 0x32  #原为0x02
CT_FILETYPE     = 0x33  #原为0x03
CT_SOURCES      = 0x15
CT_COMPLSRC     = 0x30
CT_MODSTR       = 0x55
CT_UDPPORTS     = 0xf9
CT_MISCFEATURES = 0xfa

#Flags
FL_ZLIB         = 0x01
FL_IPINLOGIN    = 0x02
FL_AUXPORT      = 0x04
FL_NEWTAGS      = 0x08
FL_UNICODE      = 0x10

#Port
CPORT = 5474
SPORT = 5473

#File Type
FT_ED2K_AUDIO = "Audio"
FT_ED2K_VIDEO = "Video"
FT_ED2K_IMAGE = "Image"
FT_ED2K_DOCUMENT = "Doc"
FT_ED2K_PROGRAM = "Pro"





class Ed2k:
    host = ''
    port = None
    sock = None
    GUID = None
    cnt_users = 0
    cnt_files = 0

    server_name = "YH 1# ED2K Server"
    server_desc = "Server Desc"

    userlist    = {}
    serverlist  = {}
    filelist    = {}
    filesrc     = {}
    file2user   = {}



    def __init__ (self, host, port):
        self.host = host
        self.port = port
        self.GUID = self.user_hash()
    def listen(self):
        th = threading.Thread(target = self.__listen);
        th.setName("Thread<listen>")
        th.start()
    def __listen(self):
        """
        TODO:加入异常处理
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("localhost", self.port))
        sock.listen(5)
        print threading.currentThread().getName(),"listen on %d" % self.port
        while 1:
            infds, outfds, errfds = select.select([sock, ], [], [], 5)
            if len(infds) != 0:
                csock, caddr = sock.accept()

                t = threading.Thread(target = self.process,
                                        args = [csock,caddr])

                t.setDaemon(True)
                t.start()
#                t.join()
                #暂时让其单线程运行利于调试
                #csock.close()
            print "no data coming"
    def process(self,sock,addr):
        print threading.currentThread().getName()
#        t = threading.Thread(target = self.answer)
#        t.start()
        while 1:
            try:
                buf = sock.recv(4096)
            except socket.error, e:
                self.error(e,"连接中断")
#            print "【%s】%s 【from】 %s " % (ctime(),repr(buf),addr)
            self.parser(sock,buf,len(buf))
#            print "ok"
#            sock.send("hello ansewr")"
        pass
    def parser(self,sock,buf,length):
        index = 0
        while(index < length):
            proto = struct.unpack("!B", buf[index])[0]
            index += 1
#            print proto
            if proto == PR_ED2K:
                packlen = struct.unpack("!I",buf[index:index+4])[0]
                index += 4
                opcode = struct.unpack("!B", buf[index])[0]
                index += 1
#                print opcode
                self.OpHandler[opcode](self,sock,buf[index:index+packlen])
                index += packlen


    def error(self,e,str):
        print "%s : %s" % (e,str)
        sys.exit(1)
    def answer(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 5474))
        while 1:
            sock.send("answer")
            buf = sock.recv(1024)
            sleep(2)
    def hello(self,addr):
        th = threading.Thread(target = self.__hello,
                                args = [addr]);
        th.setName("Thread<hello>")
        th.start()
    def __hello(self,addr):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(addr)
        except socket.error, e:
            print "can not connect"
            sys.exit(1)
        self.sock = sock
        print threading.currentThread().getName(),"connected %s" % repr(addr)
        buf = self.pack_ED2K(self.op_Hello())
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
        pass
    def pack_ED2K(self,buf):
        fmt = "!BI"
        #print struct.calcsize(buf[-1])

        li = [PR_ED2K, struct.calcsize(buf[-1])]
        fmt += buf[-1][1:] #为了防止它自动对齐，先以网络字节序取长度，然后去掉最开头的感叹号

        for i in range(len(buf)-1):
            li.append(buf[i])

#        print fmt
#        print li
        return apply(struct.pack,(fmt,) + tuple(li))
    
    #OP Code Handler
    def hLoginRequest(self,sock,buf):
#        print repr(buf)
        info = {"sock":sock}
        index = 16
        hash = struct.unpack("!16s",buf[0:index])[0]
        ip = socket.inet_ntoa(struct.unpack("!4s", buf[index:index+4])[0])
        index += 4
        port = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        tags = struct.unpack("!I", buf[index:index+4])[0]
        index += 4
        info["ip"] = ip
        info["port"] = port
        info["hash"] = hash
        
        for i in range(tags):
            tagcode = struct.unpack("!B", buf[index])[0]
            index += 1
            relt = self.CtHandler[tagcode](self,buf[index:])
            index += relt[0]
            info[relt[1]] = relt[2]
        self.userlist[hash] = info
        print "userlist[hash] : ",self.userlist[hash]
        self.cnt_users +=1
        sock.send(self.pack_ED2K(self.op_ServerMessage("I am Server Msg!")))
        sock.send(self.pack_ED2K(self.op_ServerStatus()))
#        print repr(self.pack_ED2K(self.op_ServerStatus()))
        sock.send(self.pack_ED2K(self.op_IDChange(self.client_hash(sock.getpeername()[0]))))
#        print repr(self.pack_ED2K(self.op_IDChange(self.client_hash(sock.getpeername()[0]))))

    def hServerMessage(self,sock,buf):
        index = 0
        len = struct.unpack("!H",buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        msg = struct.unpack(fmt,buf[index:index+len])[0]
        print "Server Msg :: %s" % msg
        
    def hServerStatus(self,sock,buf):
        index = 0
        cnt_users = struct.unpack("!I",buf[index:index+4])[0]
        index += 4
        cnt_files = struct.unpack("!I",buf[index:index+4])[0]
        print "Server users : %d  And files : %d" %(cnt_users,cnt_files)
    def hIDChange(self,sock,buf):
        newid = struct.unpack("!I",buf[0:4])
        print "NewID : %d" % newid
    def hServerList(self,sock,buf):
        pass
    def hGetServerList(self,sock,buf):
        sock.send(self.pack_ED2K(self.op_ServerIdent()))
        pass
    def hServerIdent(self,sock,buf):
        info = {}
        index = 0
        hash = struct.unpack("!16s",buf[index:index+16])[0]
        index +=16
        ip = socket.inet_ntoa(struct.unpack("!4s", buf[index:index+4])[0])
        index += 4
        port = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        tags = struct.unpack("!I", buf[index:index+4])[0]
        index += 4
        
        info["ip"] = ip
        info["port"] = port
        for i in range(tags):
            tagcode = struct.unpack("!B", buf[index])[0]
            index += 1
            relt = self.CtHandler[tagcode](self,buf[index:])
            index += relt[0]
            info[relt[1]] = relt[2]
        self.serverlist[hash] = info
        print "ServerIdent : ",self.serverlist[hash]
    def hOfferFiles(self,sock,buf):
#        print "hOfferFiles"
        
        index = 0
        cnt = struct.unpack("!I",buf[index:index+4])[0]
        index +=4
        for i in range(cnt):
            info = {}
            host = {}
            hash = struct.unpack("!16s",buf[index:index+16])[0]
            index +=16
            ip = struct.unpack("!4s", buf[index:index+4])[0]
            index += 4
            port = struct.unpack("!H", buf[index:index+2])[0]
            index += 2
            tags = struct.unpack("!I", buf[index:index+4])[0]
            index += 4
    #        print repr(hash)
            info["hash"] = hash
            info["ip"] = ip
            info["port"] = port
#            host["ip"] = ip
#            host["port"] = port
#            if hash in self.file2user:
#
            if hash in self.filelist :
#                print type(self.filelist[hash]["src"])
                self.filelist[hash]["src"] +=1
                self.filelist[hash]["complsrc"] +=1
            else:
                info["src"] = int(1)
                info["complsrc"] = int(1)
                self.filelist[hash] = info
                self.cnt_files += 1

#            print self.filelist[hash]

            for i in range(tags):
                tagcode = struct.unpack("!B", buf[index])[0]
                index += 1
                relt = self.CtHandler[tagcode](self,buf[index:])
                index += relt[0]
                info[relt[1]] = relt[2]
            
#            print self.filelist[hash]
#        for file in self.filelist:
#            print self.filelist[file]
    def hSearch(self,sock,buf):
        index = 0
        relt = []
        len = struct.unpack("!H",buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        expr = struct.unpack(fmt,buf[index:index+len])[0]
        for file in self.filelist:
            m = re.match(expr, self.filelist[file]["name"])
            if m :
                relt.append(file)
                print "match search: ",m.group()
        sock.send(self.pack_ED2K(self.op_SearchResult(relt)))
#        print "SearchExpr :: %s" % expr
    def hSearchResult(self,sock,buf):
        index = 0
        cnt = struct.unpack("!I",buf[index:index+4])[0]
        index +=4
        for i in range(cnt):
            info = {}
            hash = struct.unpack("!16s",buf[index:index+16])[0]
            index +=16
            ip = struct.unpack("!4s", buf[index:index+4])[0]
            index += 4
            port = struct.unpack("!H", buf[index:index+2])[0]
            index += 2
#            print repr(ip),port
            tags = struct.unpack("!I", buf[index:index+4])[0]
            index += 4
            info["hash"] = hash
            info["ip"] = ip
            info["port"] = port

            for i in range(tags):
                tagcode = struct.unpack("!B", buf[index])[0]
                index += 1
                relt = self.CtHandler[tagcode](self,buf[index:])
                index += relt[0]
                info[relt[1]] = relt[2]

#            print info
            print "ed2k://|file|",info["name"],"|",info["size"],"|",struct.unpack("16B",info["hash"]),"|/"
        pass

    def h_Hello(self,sock,buf):
        info = {"sock":sock}
        index = 16
        hash = struct.unpack("!16s",buf[0:index])[0]
        ip = socket.inet_ntoa(struct.unpack("!4s", buf[index:index+4])[0])
        index += 4
        port = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        tags = struct.unpack("!I", buf[index:index+4])[0]
        index += 4
        info["ip"] = ip
        info["port"] = port
        info["hash"] = hash

        for i in range(tags):
            tagcode = struct.unpack("!B", buf[index])[0]
            index += 1
            relt = self.CtHandler[tagcode](self,buf[index:])
            index += relt[0]
            info[relt[1]] = relt[2]
        self.userlist[hash] = info
        print "userlist[hash] : ",self.userlist[hash]
        self.cnt_users +=1
        sock.send(self.pack_ED2K(self.op_HelloAnswer()))
    def h_HelloAnswer(self,sock,buf):
        info = {"sock":sock}
        index = 1
        hash = struct.unpack("!B",buf[0:index])[0]
        #hash==0x0f 表示helloanswer
        ip = socket.inet_ntoa(struct.unpack("!4s", buf[index:index+4])[0])
        index += 4
        port = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        tags = struct.unpack("!I", buf[index:index+4])[0]
        index += 4
        info["ip"] = ip
        info["port"] = port
#        info["hash"] = hash

        for i in range(tags):
            tagcode = struct.unpack("!B", buf[index])[0]
            index += 1
            relt = self.CtHandler[tagcode](self,buf[index:])
            index += relt[0]
            info[relt[1]] = relt[2]
#        self.userlist[hash] = info
        print "info : ",info
    def h_ReqFile(self,sock,buf):
        index = 0
        hash = struct.unpack("!16s",buf[index:index+16])[0]
        index +=16
        print hash
    def h_FileName(self,sock,buf):
        index = 0
        hash = struct.unpack("!16s",buf[index:index+16])[0]
        index +=16
        len = struct.unpack("!I",buf[index:index+4])[0]
        index += 4
        fmt = "!%ds" % len
        name = struct.unpack(fmt,buf[index:index+len])[0]
    def h_FileDesc(self,sock,buf):
        index = 0
        rating = struct.unpack("!B",buf[index:index+1])[0]
        index +=1
        len = struct.unpack("!I",buf[index:index+4])[0]
        index += 4
        fmt = "!%ds" % len
        comment = struct.unpack(fmt,buf[index:index+len])[0]
    def h_SetReqFileID(self,sock,buf):
        index = 0
        hash = struct.unpack("!16s",buf[index:index+16])[0]
        index +=16
    def h_ReqFile_Status(self,sock,buf):
        index = 0
        hash = struct.unpack("!16s",buf[index:index+16])[0]
        index +=16
        count = struct.unpack("!B",buf[index:index+2])[0]
        index +=2
#        for i in range(count):
    def h_ReqFile_NoFile(self,sock,buf):
        index = 0
        hash = struct.unpack("!16s",buf[index:index+16])[0]
        index +=16
        pass
    def h_ReqHashSet(self,sock,buf):
        index = 0
        hash = struct.unpack("!16s",buf[index:index+16])[0]
        index +=16
        pass
    def h_HashSet(self,sock,buf):
        index = 0
        hash = struct.unpack("!16s",buf[index:index+16])[0]
        index +=16
        cnt = struct.unpack("!B",buf[index:index+2])[0]
        index +=2
    def h_StartUploadReq(self,sock,buf):
        index = 0
        hash = struct.unpack("!16s",buf[index:index+16])[0]
        index +=16
    def h_AcceptUploadReq(self,sock,buf):
        pass
    def h_QueueRanking(self,sock,buf):
        index = 0
        ranking = struct.unpack("!I",buf[index:index+4])[0]
        index +=4
        pass
    def h_ReqChunks(selfm,sock,buf):
        index = 0
        hash = struct.unpack("!16s",buf[index:index+16])[0]
        index +=16
        begins = []
        ends = []
        for i in range(3):
            begin = struct.unpack("!16s",buf[index:index+4])[0]
            index +=4
            begins.append(begin)
        for i in range(3):
            end = struct.unpack("!16s",buf[index:index+4])[0]
            index +=4
            begins.append(end)
        pass
    def h_SendingChunk(self,sock,buf):
        index = 0
        hash = struct.unpack("!16s",buf[index:index+16])[0]
        index +=16
        begin = struct.unpack("!16s",buf[index:index+4])[0]
        index +=4
        end = struct.unpack("!16s",buf[index:index+4])[0]
        index +=4
        fmt = "!%ds" % (end-begin)
        data = struct.unpack(fmt,buf[index:index+end-begin])[0]
    def h_CancelTransfer(self,sock,buf):
        pass


    """
    CT Code Handler
    """
    def hNICK(self,buf):
        index = 0
        len = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        nick = struct.unpack(fmt,buf[index:index+len])[0]
#        self.userlist[hash]["nick"] = nick
        return [index+len,"nick",nick]
    def hVERSION(self,buf):
        ver = struct.unpack("!B", buf[0])[0]
#        self.userlist[hash]["version"] = ver
        return [1,"version",ver]
    def hPORT(self,buf):
        port = struct.unpack("!H", buf[0:2])[0]
#        self.userlist[hash]["port"] = port
        return [2,"port",port]
    def hMULEVERSION(self,buf):
        mul = struct.unpack("!I", buf[0:4])[0]
#        self.userlist[hash]["muleversion"] = mul
        return [4,"muleversion",mul]
    def hFLAGS(self,buf):
        flags = struct.unpack("!B", buf[0])[0]
#        self.userlist[hash]["flags"] = flags
        return [1,"flags",flags]
    def hSERVERNAME(self,buf):
        index = 0
        len = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        name = struct.unpack(fmt,buf[index:index+len])[0]
#        self.serverlist[hash]["name"] = name
        return [index+len,"name",name]
    def hSERVERDESC(self,buf):
        index = 0
        len = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        desc = struct.unpack(fmt,buf[index:index+len])[0]
#        self.serverlist[hash]["desc"] = desc
        return [index+len,"desc",desc]
    def hFILENAME(self,buf):
        index = 0
        len = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        name = struct.unpack(fmt,buf[index:index+len])[0]
#        self.filelist[hash]["name"] = name
        return [index+len,"name",name]
    def hFILESIZE(self,buf):
        size = struct.unpack("!I",buf[0:4])[0]
#        self.filelist[hash]["size"] = size
        return [4,"size",size]
    def hFILETYPE(self,buf):
        index = 0
        len = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        type = struct.unpack(fmt,buf[index:index+len])[0]
#        self.filelist[hash]["type"] = str
        return [index+len,"type",type]
    def hSOURCES(self,buf):
        src = struct.unpack("!I",buf[0:4])[0]
#        self.filelist[hash]["src"] = src
        return [4,"src",src]
    def hCOMPLSRC(self,buf):
        complsrc = struct.unpack("!I",buf[0:4])[0]
#        self.filelist[hash]["complsrc"] = complsrc
        return [4,"complsrc",complsrc]
    def hMODSTR(self,buf):
        index = 0
        len = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        modstr = struct.unpack(fmt,buf[index:index+len])[0]
        return [index+len,"modstr",modstr]
    def hUDPPORTS(self,buf):
        kad = struct.unpack("!H",buf[0:2])[0]
        ed2k = struct.unpack("!H",buf[2:4])[0]
        return [4,"kadudpport",kad,"ed2kudpport",ed2k]
    def hMISCFEATURES(self,buf):
        bitset = struct.unpack("!I",buf[0:4])[0]
        return [4,"fetures",bitset]

    #Tools
    def user_hash(self):
        li = []
        for i in range(16):
            li.append(random.randint(0,255))
        li[5] = 14
        li[14] = 111

#        print li
        return apply(struct.pack,("16B",) + tuple(li))
    def client_hash(self,ip):
        tID = socket.inet_aton(ip)
        ID = struct.unpack("=I",tID)[0]
#        print "client hash"ID
        return ID

    ##Tags
    def ct_NICK(self,nick):
        fmt = "BH%ds" % len(nick)
        return [fmt, CT_NICK, len(nick),nick]
    def ct_VERSION(self):
        fmt = "BB"
        return [fmt,CT_VERSION,0x3c]
    def ct_PORT(self,port):
        fmt = "BH"
        return [fmt,CT_PORT,port]
    def ct_MULEVERSION(self,ver):
        fmt = "BI"
        return [fmt,CT_MULEVERSION,ver]
    def ct_FLAGS(self,flags):
        fmt = "BB"
        return [fmt,CT_FLAGS,flags]
    def ct_SERVERNAME(self,str):
        fmt = "BH%ds" % len(str)
        return [fmt,CT_SERVERNAME,len(str),str]
    def ct_SERVERDESC(self,str):
        fmt = "BH%ds" % len(str)
        return [fmt,CT_SERVERDESC,len(str),str]
    def ct_FILENAME(self,name):
        fmt = "BH%ds" % len(name)
        return [fmt, CT_FILENAME, len(name),name]
    def ct_FILESIZE(self,size):
        fmt = "BI"
        return [fmt, CT_FILESIZE, size]
    def ct_FILETYPE(self,type):
        fmt = "BH%ds" % len(type)
        return [fmt, CT_FILETYPE, len(type),type]
    def ct_SOURCES(self,src):
        fmt = "BI"
        return [fmt, CT_SOURCES, src]
    def ct_COMPLSRC(self,complsrc):
        fmt = "BI"
        return [fmt, CT_COMPLSRC, complsrc]
    def ct_MODSTR(self,str):
        fmt = "BH%ds" % len(str)
        return [fmt,CT_MODSTR,len(str),str]
    def ct_UDPPORTS(self,kad,udp):
        fmt = "BHH"
        return [fmt,CT_UDPPORTS,kad,udp]
    def ct_MISCFEATURES(self,bitset):
        fmt = "BI"
        return [fmt,CT_MISCFEATURES,bitset]

    def op_Hello(self):
        fmt = "!B16s4sHI"
        li = [OP_HELLO]
        li.append(self.GUID)
        li.append(socket.inet_aton(socket.gethostbyname(self.host)))
        li.append(self.port)
        li.append(6)

        buf = self.ct_NICK("YH_SCU")
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_VERSION()
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_PORT(self.port)
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_MODSTR("ydonkey")
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_UDPPORTS(0,0)
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_MISCFEATURES(1234)
        fmt += buf[0]
        li.extend(buf[1:])

        li.append(fmt)
#        print li
#        return apply(struct.pack,(fmt,) + tuple(li))
        return li
    def op_HelloAnswer(self):
        fmt = "!BB4sHI"
        li = [OP_HELLOANSWER]
        li.append(0x0f)
        li.append(socket.inet_aton(socket.gethostbyname(self.host)))
        li.append(self.port)
        li.append(6)

        buf = self.ct_NICK("YH_SCU")
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_VERSION()
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_PORT(self.port)
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_MODSTR("ydonkey")
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_UDPPORTS(0,0)
        fmt += buf[0]
        li.extend(buf[1:])

        buf = self.ct_MISCFEATURES(1234)
        fmt += buf[0]
        li.extend(buf[1:])

        li.append(fmt)
#        print li
#        return apply(struct.pack,(fmt,) + tuple(li))
        return li

    #OP Code To Handler
    OpHandler ={OP_LOGINREQUEST:hLoginRequest,
                OP_SERVERMESSAGE:hServerMessage,
                OP_SERVERSTATUS:hServerStatus,
                OP_IDCHANGE:hIDChange,
                OP_GETSERVERLIST:hGetServerList,
                OP_SERVERLIST:hServerList,
                OP_SERVERIDENT:hServerIdent,
                OP_OFFERFILES:hOfferFiles,
                OP_SEARCH:hSearch,
                OP_SEARCHRESULT:hSearchResult,
                OP_REQFILE:h_ReqFile,
                OP_FILENAME:h_FileName,
                OP_FILEDESC:h_FileDesc,
                OP_SETREQFILEID:h_SetReqFileID,
                OP_REQFILE_STATUS:h_ReqFile_Status,
                OP_REQFILE_NOFILE:h_ReqFile_NoFile,
                OP_REQHASHSET:h_ReqHashSet,
                OP_HASHSET:h_HashSet,
                OP_STARTUPLOADREQ:h_StartUploadReq,
                OP_ACCEPTUPLOADREQ:h_AcceptUploadReq,
                OP_QUEUERANKING:h_QueueRanking,
                OP_REQCHUNKS:h_ReqChunks,
                OP_SENDINGCHUNK:h_SendingChunk,
                OP_CANCELTRANSFER:h_CancelTransfer,
                OP_HELLO:h_Hello,
                OP_HELLOANSWER:h_HelloAnswer}
    #CT To Handler
    CtHandler ={CT_NICK:hNICK,
                CT_VERSION:hVERSION,
                CT_PORT:hPORT,
                CT_MULEVERSION:hMULEVERSION,
                CT_FLAGS:hFLAGS,
                CT_SERVERNAME:hSERVERNAME,
                CT_SERVERDESC:hSERVERDESC,
                CT_FILENAME:hFILENAME,
                CT_FILESIZE:hFILESIZE,
                CT_FILETYPE:hFILETYPE,
                CT_SOURCES:hSOURCES,
                CT_COMPLSRC:hCOMPLSRC,
                CT_MODSTR:hMODSTR,
                CT_UDPPORTS:hUDPPORTS,
                CT_MISCFEATURES:hMISCFEATURES}
