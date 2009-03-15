## coding=utf-8
__author__="qianjin"
__date__ ="$2009-3-3 13:36:58$"

if __name__ == "__main__":
    print "Hello";

class Parent:
    __name = "parent name"
    def __init__(self,str):
        print str
    def func_1(self,str):
        print str
    def __fun_2(self):
        print "private func"
        
class Child(Parent):
    def __init__(self):
        Parent.__init__(self,"good parent")
        Parent.func_1(self,"good func_1")
        print "good child"

    def Attribute(self):
#        print Parent.__name //类私有不得访问
        pass
    
cl = Child()
cl.Attribute()
#print cl.__name //类私有不得访问
