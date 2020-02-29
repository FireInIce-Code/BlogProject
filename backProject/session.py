from pyDatabase import database
import json
import hashlib
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
    if len(ds) == 0:  # 如果还没有会话
        db.create("session", sessionId=sessionId, value=jdata)  # 创建
    else:  # 否则
        d = ds[0]  # 获取会话
        d.value = jdata  # 设置值
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
        #返回,并把其中的"%"替换为双引号
        return json.loads(ds[0].value.replace("%", "\""))
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
