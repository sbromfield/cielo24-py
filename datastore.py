import sqlite3
import sys
import os

class datastore:



    def __init__(self):
        print "Set up database"
        self.addr = os.path.dirname(os.path.realpath(sys.argv[0]))
        try:
            self.newdb = not os.path.exists(self.addr + '/data.db')
            self.con = sqlite3.connect(self.addr + '/data.db')
            self.cur = self.con.cursor()

        except:
            print "Error with DB"
            sys.exit(1)

    def loadtables(self):
        if self.newdb:
            print "loading tables into the db!"
            with open(self.addr + "/schema.sql", 'rt') as f:
                schema = f.read()
                self.con.executescript(schema)
        else:
            print "database exists and has tables!"

    def addnew(self, videos):
        for video in videos:
            sql = "select id, path, status from files where path = ?"
            self.cur.execute(sql, (video,))

            if len(self.cur.fetchall()) == 0:
                print "Nothing matching " + video
                sql2 = "insert into files(status,path) values('pending', ?)"
                self.cur.execute(sql2, (video,))
            else:
                print "Is present"

    def getallpending(self):
        sql = "select * from files where status = 'pending'"
        self.cur.execute(sql)
        return self.cur.fetchall()

    def getinfo(self, path):
        sql = "select * from files where path = ?"
        self.cur.execute(sql, (path,))
        return self.cur.fetchall()

    def setrowinfo(self,path,  status, jobid, taskid):
        sql = "update files set status = ?, jobid = ?, processid = ? where path = ? "
        self.cur.execute(sql, (status,jobid, taskid, path,))
        self.con.commit()

    def setrowstatus(self,path,  status):
        sql = "update files set status = ? where path = ? "
        self.cur.execute(sql, (status, path,))
        self.con.commit()


    def getallprocessing(self):
        sql = "select * from files where status = 'processing'"
        self.cur.execute(sql)
        return self.cur.fetchall()
    def close(self):
        self.con.close()
