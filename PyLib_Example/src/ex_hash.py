
__author__="yh"
__date__ ="$2009-3-3 0:46:02$"

if __name__ == "__main__":
    print "Hello";

import random
import struct

li = []
for i in range(16):
    li.append(random.randint(0,255))

print apply(struct.pack,("16B",) + tuple(li))

