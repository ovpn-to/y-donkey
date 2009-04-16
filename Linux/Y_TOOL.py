
__author__="qianjin"
__date__ ="$2009-3-26 15:48:00$"

if __name__ == "__main__":
    print "Hello";

class Files:
    filelist = {}
    def __init__(self):
        pass
    def addFile(self,file):
        filelist[file["hash"]] = tiem
        pass
    def delFile(self,hash):

        pass
    def isFile(self,hash):
        return hash in filelist
    def getFiles(self,hash):
        return filelist.get(hash)
    def search(self,expr):
        return files
