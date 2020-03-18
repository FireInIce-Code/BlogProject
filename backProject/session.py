from pyDatabase import database
import json
import hashlib
import time
sessionCount = 0  # 会话数量,用于存储会话
db = None


def init(database):
    global db
    db = database  # 设定数据库

# 设置会话内容


def setSession(sessionId, valueDict):
    jdata = json.dumps(valueDict).replace("\"", "%")  # json序列化内容,并把双引号替换成"%"
    # 获取数据库中sessionId为sessionId的会话
    ds = db.filter("session", sessionId=sessionId)
    currentTime=time.time()  #当前时间
    delTime=int(currentTime)+60*60*24  #删除时间
    if len(ds) == 0:  # 如果还没有会话
        db.create("session", sessionId=sessionId, value=jdata, delTime=delTime)  # 创建
    else:  # 否则
        d = ds[0]  # 获取会话
        d.value = jdata  # 设置值
        d.delTime=delTime
        d.save()  # 保存

# 获取会话
def getSession(sessionId):
    # 如果会话id是空的,返回空
    if sessionId == None:
        return None
    #获取sessionId为sessionId的会话
    ds = db.filter("session", sessionId=sessionId)
    #如果存在
    if len(ds) == 1:
        d=ds[0]  #会话数据
        currentTime=time.time()  #当前时间
        if d.delTime>currentTime:
            d.delTime=currentTime+60*60*24
            #返回,并把其中的"%"替换为双引号
            return json.loads(ds[0].value.replace("%", "\""))
        else:
            d.delete()
            return None
    else:
        #没有则返回空
        return None

#删除会话
def removeSession(sessionId):
    global db
    #获取会话
    ds = db.filter("session", sessionId=sessionId)
    #如果存在
    if len(ds) == 1:
        #删除
        db.remove("session", sessionId=sessionId)
        #保存
        db.save()

#创建一个会话ID
def newSessionId():
    #将sessionCount+1
    global sessionCount
    sessionCount += 1
    #返回根据sessionCount生成的会话ID
    return hashlib.md5(bytes(str(sessionCount), encoding="utf-8")).hexdigest()
