
__author__="qianjin"
__date__ ="$2009-3-24 15:11:03$"

if __name__ == "__main__":
    print "Hello";

import os
import os.path

print os.name

#print os.path.abspath("d:/")
#print os.path.dirname("d:\\download")
#os.chdir("d:\\")

for root,dirs,files in os.walk("d:\download"):
    print root,dirs
    for file in files:
        print file
