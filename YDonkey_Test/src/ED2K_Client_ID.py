
__author__="qianjin"
__date__ ="$2009-3-12 10:41:23$"

if __name__ == "__main__":
    print "Hello";

import ED2K_BASE
import ED2K

#ed = ED2K_BASE.Ed2k()

#print ed.client_hash("192.168.10.1")

client = ED2K.Ed2kClient()

client.initFileTable()

client.offerFile(1)