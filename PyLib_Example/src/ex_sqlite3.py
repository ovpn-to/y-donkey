
__author__="qianjin"
__date__ ="$2009-3-18 13:26:54$"

if __name__ == "__main__":
    print "Hello";

import sqlite3

initSQLs=[ "create table IF NOT EXISTS files(hash text not null primary key,\
                                name text not null,\
                                src integer not null default 0,\
                                complsrc integer not null default 0,\
                                type text)",
            "create table IF NOT EXISTS users(hash text not null primary key,\
                                name text not null,\
                                version text not null,\
                                port integer not null,\
                                mulversion text,\
                                flag text)",
            "create table IF NOT EXISTS servers(hash text not null primary key,\
                                name text not null,\
                                desc text)"]

conn = sqlite3.connect('database')

c = conn.cursor()


for i in initSQLs:
    c.execute(i)

c.execute('insert into files(hash,name,src) values("DAFDFSDGVDG","dsadsadas",10)')
c.execute('insert into files(hash,name) values("DAFDFSDGSDG","dsadsadas")')

conn.commit()
c.execute('select * from files')
for row in c:
    for i in row:
        print i


# We can also close the cursor if we are done with it
c.close()

