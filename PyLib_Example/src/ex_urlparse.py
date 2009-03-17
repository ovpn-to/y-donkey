
__author__="qianjin"
__date__ ="$2009-3-17 17:45:11$"

if __name__ == "__main__":
    print "Hello";

from urlparse import *

o = urlparse('http://192.168.30.107/report.html?tag=kongzhi20090226k86&time=2009-03-08,00:10:01&hostname=item1.cm3&type=load&name=&value=1.76')[4]

print o
print urlsplit("http://192.168.30.107/report.html?tag=kongzhi20090226k86&time=2009-03-08,00:10:01&hostname=item1.cm3&type=load&name=&value=1.76")
qs = parse_qsl(o)
print type(qs)
