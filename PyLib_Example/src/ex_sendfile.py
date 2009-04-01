
__author__="qianjin"
__date__ ="$2009-3-31 17:13:51$"

if __name__ == "__main__":
    print "Hello";


fd = open("2009-03-08-taobao-access_log","rb")

fd.seek(1)
block = fd.read(640)

print block