from parse import parsejson
from httprequests import httprequests
from datastore import datastore
from folder import folder
import datetime
'''
Quick and dirty hack by stephen to add cc to course capture videos 
Need to add better error handling 
'''
if __name__ == "__main__":
  print "Starting..."
  config = parsejson()
  db = datastore()
  db.loadtables()
  myrequests = httprequests(config.config)
  myrequests.login()
  try:
      while 1:
          for k,p in config.dirs.iteritems():
              #print p
              f = folder(p)
              f.load()
              db.addnew(f.hasvideo())
              pending = db.getallpending()
              #myrequests.createjob()
              for pend in pending:
                  print p
                  print "-----"
                  info = myrequests.createjob()
                  print pend[2]
                  r = myrequests.addmedia(pend[2],info['jobid'])
                  #after upload, save the task and job id to db and change status
                  db.setrowinfo(pend[2], "uploaded", info['jobid'], r['taskid'])
                  r2 = db.getinfo(pend[2])
                  print r2
                  myrequests.perform_transcription(r2[0][4])
                  db.setrowinfo(pend[2], "processing", info['jobid'], r['taskid'])
                  print db.getinfo(pend[2])

          processing = db.getallprocessing()
          for process in processing:
              print "Processing----"
              print process
              #myrequests.info(process[4])
              t = myrequests.getduedate(myrequests.info(process[4]))

              if datetime.datetime.now() > t:
                 print "ready!"
                 localdir = process[2][0:process[2].rindex("/")]
                 name = process[2][process[2].rindex("/") + 1:-4] + ".vtt"
                 print name
                 cc = myrequests.getcaption(process[4])
                 ccfile = open(localdir + "/" + name, "w")
                 ccfile.write(cc)
                 ccfile.close()
                 db.setrowstatus(process[2], "done")
              else:
                 print "not ready"

          break


  except KeyboardInterrupt:
      print "\n exiting"
  db.close()
