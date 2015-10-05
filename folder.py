import os

class folder:

    def __init__(self, p):
         self.path = p
         self.files = os.listdir(p)
         self.subfolders = []

    def load(self):
        for x in self.files:
            if os.path.isdir(self.path + "/" + x):
                self.subfolders.append(self.path + "/" + x)
        #print self.subfolders

    def hasvideo(self):
        r = []
        for p in self.subfolders:
            #print p + "---"
            temp = os.listdir(p)
            for x in temp:
                if ".mp4" in x:
                     r.append(p + "/" + x)

        return r
