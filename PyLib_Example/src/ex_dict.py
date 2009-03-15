## coding:utf-8 ##
__author__="qianjin"
__date__ ="$2009-3-3 19:14:09$"

if __name__ == "__main__":
    print "Hello";


def func():
    print "func"

#dictionary容器可以放置任何数据类型
dict = {1:func,2:func}

dict[1]()
dict[2]()

print type(func)