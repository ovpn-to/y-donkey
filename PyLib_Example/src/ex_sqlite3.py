
__author__="qianjin"
__date__ ="$2009-3-18 13:26:54$"

if __name__ == "__main__":
    print "Hello";

import sqlite3

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute('create table files (hash text,name text,src integer)')
c.execute('insert into files values("DAFDFSDGSDG","dsadsadas",10)')

c.execute('select * from files')
for row in c:
    print row


# We can also close the cursor if we are done with it
c.close()

