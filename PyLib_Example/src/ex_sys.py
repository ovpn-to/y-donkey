
__author__="qianjin"
__date__ ="$2009-3-16 18:37:13$"

if __name__ == "__main__":
    print "Hello";



#buf = sys.stdin.readline()


def login(str):
    print str


Handle = {"login":login}

while True :
    buf = raw_input()
    Handle[buf](buf)