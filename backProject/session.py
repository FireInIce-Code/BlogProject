import json
import hashlib
sessionCount=0
from pyDatabase import database
def init(database):
    global db
    db=database

def setSession(sessionId,valueDict):
    jdata=json.dumps(valueDict).replace("\"","%")
    ds=db.filter("session",sessionId=sessionId)
    if len(ds)==0:
        db.create("session",sessionId=sessionId,value=jdata)
    else:
        d=ds[0]
        d.value=jdata
        d.save()

def getSession(sessionId):
    if sessionId==None:return None
    ds=db.filter("session",sessionId=sessionId)
    if len(ds)==1:
        return json.loads(ds[0].value.replace("%","\""))
    else:
        return None

def removeSession(sessionId):
    db=db.filter("session",sessionId=sessionId)
    if len(ds)==1:
        db.remove("session",sessionId=sessionId)
        db.save()

def newSessionId():
    global sessionCount
    sessionCount+=1
    return hashlib.md5(bytes(str(sessionCount),encoding="utf-8")).hexdigest()