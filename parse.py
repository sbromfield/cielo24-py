import json
import os.path
import sys

class parsejson:

    def __init__(self):
        addr = os.path.dirname(os.path.realpath(sys.argv[0]))
		
        with open(addr + "/config.json") as c:
                self.config = json.load(c)

        with open(addr + "/dirs.json") as d:
            self.dirs = json.load(d)

    def printconfig(self):
        print self.config
