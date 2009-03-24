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
OP_HELLO        = 0x01
OP_HELLOANSWER  = 0x4C

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
    cnt_users = 100
    cnt_files = 2000

    server_name = "YH 1# ED2K Server"
    server_desc = "Server Desc"

    userlist    = {}
    serverlist  = {}
    filelist    = {}
    filesrc     = {}




    def __init__ (self, host, port):
        self.host = host
        self.port = port
        self.GUID = self.user_hash()
    def listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(5)
        while 1:
            infds, outfds, errfds = select.select([self.sock, ], [], [], 5)
            if len(infds) != 0:
                csock, caddr = self.sock.accept()

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
#            sock.send("hello ansewr")
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
        self.userlist[hash] = info
        info["ip"] = ip
        info["port"] = port
        for i in range(tags):
            tagcode = struct.unpack("!B", buf[index])[0]
            index += 1
            index += self.CtHandler[tagcode](self,buf[index:],hash)
        print self.userlist[hash]
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
        self.serverlist[hash] = info
        info["ip"] = ip
        info["port"] = port
        for i in range(tags):
            tagcode = struct.unpack("!B", buf[index])[0]
            index += 1
            index += self.CtHandler[tagcode](self,buf[index:],hash)
        print self.serverlist[hash]
    def hOfferFiles(self,sock,buf):
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
        self.filelist[hash] = info
        info["ip"] = ip
        info["port"] = port
        for i in range(tags):
            tagcode = struct.unpack("!B", buf[index])[0]
            index += 1
            index += self.CtHandler[tagcode](self,buf[index:],hash)
        print self.filelist[hash]
    def hSearch(self,sock,buf):
        index = 0
        len = struct.unpack("!H",buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        expr = struct.unpack(fmt,buf[index:index+len])[0]
        print "SearchExpr :: %s" % expr
    def hSearchResult(self,sock,buf):
        pass


    #CT Code Handler
    def hNICK(self,buf,hash):
        index = 0
        len = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        nick = struct.unpack(fmt,buf[index:index+len])[0]
        self.userlist[hash]["nick"] = nick
        return index+len
    def hVERSION(self,buf,hash):
        ver = struct.unpack("!B", buf[0])[0]
        self.userlist[hash]["version"] = ver
        return 1
    def hPORT(self,buf,hash):
        port = struct.unpack("!H", buf[0:2])[0]
        self.userlist[hash]["port"] = port
        return 2
    def hMULEVERSION(self,buf,hash):
        mul = struct.unpack("!I", buf[0:4])[0]
        self.userlist[hash]["muleversion"] = mul
        return 4
    def hFLAGS(self,buf,hash):
        flags = struct.unpack("!B", buf[0])[0]
        self.userlist[hash]["flags"] = flags
        return 1
    def hSERVERNAME(self,buf,hash):
        index = 0
        len = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        name = struct.unpack(fmt,buf[index:index+len])[0]
        self.serverlist[hash]["name"] = name
        return index+len
    def hSERVERDESC(self,buf,hash):
        index = 0
        len = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        desc = struct.unpack(fmt,buf[index:index+len])[0]
        self.serverlist[hash]["desc"] = desc
        return index+len
    def hFILENAME(self,buf,hash):
        index = 0
        len = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        str = struct.unpack(fmt,buf[index:index+len])[0]
        self.filelist[hash]["name"] = str
        return index+len
    def hFILESIZE(self,buf,hash):
        size = struct.unpack("!I",buf[0:4])[0]
        self.filelist[hash]["size"] = size
        return 4
    def hFILETYPE(self,buf,hash):
        index = 0
        len = struct.unpack("!H", buf[index:index+2])[0]
        index += 2
        fmt = "!%ds" % len
        str = struct.unpack(fmt,buf[index:index+len])[0]
        self.filelist[hash]["type"] = str
        return index+len
    def hSOURCES(self,buf,hash):
        src = struct.unpack("!I",buf[0:4])[0]
        self.filelist[hash]["src"] = src
        return 4
    def hCOMPLSRC(self,buf,hash):
        complsrc = struct.unpack("!I",buf[0:4])[0]
        self.filelist[hash]["somplsrc"] = complsrc
        return 4

    #Tools
    def user_hash(self):
        li = []
        for i in range(16):
            li.append(random.randint(0,255))
        li[5] = 14
        li[14] = 111
        return li
    def client_hash(self,ip):
        tID = socket.inet_aton(ip)
        ID = struct.unpack("=I",tID)[0]
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
        return [fmt, CT_NICK, len(type),type]
    def ct_SOURCES(self,src):
        fmt = "BI"
        return [fmt, CT_FILESIZE, src]
    def ct_COMPLSRC(self,complsrc):
        fmt = "BI"
        return [fmt, CT_FILESIZE, complsrc]
    
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
                OP_SEARCHRESULT:hSearchResult}
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
                CT_COMPLSRC:hCOMPLSRC}
