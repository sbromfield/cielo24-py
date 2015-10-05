import requests
import json
import datetime

class httprequests(object):
    """docstring for """

    def __init__(self, config):
        print "http requests"
        self.config = config
        self.loginurl = "api/account/login"
        self.createjoburl = "api/job/new"
        self.addmediaurl = "api/job/add_media"
        self.performtrans = "api/job/perform_transcription"
        self.infourl = "api/job/info"
        self.captionurl = "api/job/get_caption"

    def login(self):
        r = requests.get(self.config['apiurl'] + self.loginurl +
        "?v=" + self.config["verison"] + "&username=" +
         self.config['username'] + "&password=" + self.config["pw"])

        data = json.loads(r.text)
        self.apitoken = data['ApiToken']
        print "ApiToken " + self.apitoken

    def createjob(self):
        print "creating an api job"
        r = requests.get(self.config['apiurl'] + self.createjoburl +
        "?v=" + self.config["verison"]  + "&api_token=" + self.apitoken)

        data = json.loads(r.text)
        return { "jobid" : data['JobId'],  "taskid" : data['TaskId'] }

    def addmedia(self, path, jobid):
        print "Adding media to request"
        #print self.config['apiurl'] + self.addmediaurl + "?v=" + self.config["verison"]  + "&api_token=" + self.apitoken + "&job_id=" + jobid
        with  open(path, 'rb') as f:
            r = requests.post(self.config['apiurl'] + self.addmediaurl +
        "?v=" + self.config["verison"]  + "&api_token=" + self.apitoken +
        "&job_id=" + jobid, data=f, headers={'Content-Type': 'video/mp4'})
        #print r.request.headers
        data  = json.loads(r.text)
        return {"taskid" : data['TaskId']}

    def perform_transcription(self, jobid):
        print "performing transcription"
        r = requests.get(self.config['apiurl'] + self.performtrans + "?v=" +
        self.config["verison"]  + "&api_token=" + self.apitoken + "&job_id=" + jobid +
        "&transcription_fidelity=PROFESSIONAL&priority=STANDARD")
        print r.text

    def info(self, jobid):
        r = requests.get(self.config['apiurl'] + self.infourl + "?v=" +
        self.config["verison"]  + "&api_token=" + self.apitoken + "&job_id=" + jobid)
        return r.text

    def getcaption(self, jobid):
        r = requests.get(self.config['apiurl'] + self.captionurl + "?v=" +
        self.config["verison"]  + "&api_token=" + self.apitoken + "&job_id=" + jobid
        + "&caption_format=WEB_VTT" )

        return r.text

    def getduedate(self,data):
        print "Due dates"
        print data
        d = json.loads(data)
        tmp = d['DueDate'].split('T')
        pt = tmp[0].split('-')
        pt2 = tmp[1].split(":")
        print pt2

        time = datetime.datetime(int(pt[0]), int(pt[1]),int(pt[2]), int(pt2[0])
        , int(pt2[1]))
        return time
