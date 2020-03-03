import json
import os
import threading
import time
import hashlib
import base64
import io

import uvicorn
from fastapi import Cookie, FastAPI
from pydantic import BaseModel
from fastapi import File, UploadFile
from starlette.responses import JSONResponse, StreamingResponse

import confirmCode
import session
from pyDatabase import database

sortItems = "Python C++ Javascript Algorithm ProgrammingLife".split(" ")

app = FastAPI()
BASEDIR = os.path.dirname(__file__)
db = database.Database(os.path.join(BASEDIR, "db.sqlite3"))
session.init(db)
codes = {}


def datasToArr(blogs):
    datas = []
    for blog in blogs:
        datas.append({
            "title": blog.title,
            "id": blog.id,
            "user": blog.user,
            "date": blog.date,
            "tag": sortItems[blog.tag]
        })
    return datas


@app.get("/sortItems")
async def getSortItemsApi():
    return {
        "message": "success",
        "sortItems": sortItems
    }


class postNewBlogArg(BaseModel):
    tag: int
    inner: str
    title: str


@app.post("/blog/new")
async def postNewBlogApi(item: postNewBlogArg, sessionId=Cookie(None)):
    s = session.getSession(sessionId)
    if s:
        user = s['userId']
    else:
        return {"message": "no signIn"}
    if len(db.filter("blog", title=item.title, user=user)) != 0:
        return {"message": "repeat"}
    else:
        date = time.strftime("%Y-%m-%d")
        currentTime = int(time.time())
        db.create("blog", tag=item.tag, inner=item.inner, user=user,
                  date=date, time=currentTime, title=item.title)
    return {"message": "success"}


class postEditBlogApi(BaseModel):
    title: str
    inner: str


@app.post("/blog/new")
async def postEditBlogApi(item: postEditBlogApi, sessionId=Cookie(None)):
    s = session.getSession(sessionId)
    if s:
        user = s['userId']
    else:
        return {"message": "no signIn"}
    blogs = db.filter("blog", title=item.title, user=user)
    if len(blogs) == 1:
        blog = blogs[0]
        date = time.strftime("%Y-%m-%d")
        currentTime = int(time.time())
        blog.date = date
        blog.inner = item.inner
        blog.save()
    else:
        return {'message': "none"}
    return {"message": "success"}


class postNewGoodArg(BaseModel):
    id: int


@app.post("/blog/good")
async def postNewGoodApi(item: postNewGoodArg, sessionId=Cookie(None)):
    s = session.getSession(sessionId)
    if s:
        user = s['userId']
    else:
        return {"message": "no signIn"}
    pls = db.filter("pl", id=item.id)
    if len(pls) == 1:
        pl = pls.first()
        if user == pl.userId:
            return {
                "message": "self"
            }

        if len(db.filter("good", plId=item.id)) != 0:
            return {
                "message": "repeat"
            }

    db.create("good", plId=item.id, userId=user)
    return {"message": "success"}


class postNewPlArg(BaseModel):
    inner: str
    blog: int


@app.post("/blog/pl")
async def postNewPlApi(item: postNewPlArg, sessionId=Cookie(None)):
    s = session.getSession(sessionId)
    if s:
        user = s['userId']
    else:
        return {"message": "no signIn"}
    date = time.strftime("%Y-%m-%d")
    db.create("pl", userId=user, blogId=item.blog,
              inner=item.inner, date=date)
    return {"message": "success"}


class postSignUpArg(BaseModel):
    username: str
    nickname: str
    password: str
    code: str


@app.post("/user/signUp")
async def postSignUpApi(item: postSignUpArg, sessionId=Cookie(None)):
    c = codes.get(item.username, None)
    if not c or item.code.lower() != c.lower():
        return {"message": "code wrong"}
    else:
        codes.pop(item.username)
    if sessionId and session.getSession(sessionId):
        return {"message": "loginned"}
    if len(db.filter("user", username=item.username)) != 0:
        return {"message": "username repeat"}
    db.create("user", username=item.username,
              nickname=item.nickname, password=item.password)
    uid = db.get("user", username=item.username).id
    sessionId = session.newSessionId()
    session.setSession(sessionId, {"userId": uid})
    response = JSONResponse(content={"message": "success"})
    response.set_cookie(key="sessionId", value=sessionId, max_age=60*60)
    return response


class postSignInArg(BaseModel):
    username: str
    password: str
    code: str


@app.post("/user/signIn")
async def postSignInApi(item: postSignInArg, sessionId=Cookie(None)):
    if sessionId and session.getSession(sessionId):
        return {"message": "loginned"}
    c = codes.get(item.username, None)
    if not c or item.code.lower() != c.lower():
        return {"message": "code wrong"}
    else:
        codes.pop(item.username)
    v_user = db.filter("user", username=item.username)
    if len(v_user) != 1:
        return {"message": "failed"}
    user = v_user.first()
    if user.password == item.password:
        response = JSONResponse(content={"message": "success"})
        pd = r"{%userId%: "+str(user.id)+r"}"
        ss = db.filter("session", value=pd)
        if len(ss) == 0:
            sessionId = session.newSessionId()
            response.set_cookie(
                key="sessionId", value=sessionId, max_age=60*60)
            session.setSession(sessionId, {"userId": user.id})
            return response
        else:
            sessionId = ss.first().sessionId
            response.set_cookie(
                key="sessionId", value=sessionId, max_age=60*60)
            return response

    else:
        return {"message": "failed"}


@app.post("/user/signOut")
async def postSignOutApi(sessionId=Cookie(None)):
    s = session.getSession(sessionId)
    if s:
        session.removeSession(sessionId)
    response = JSONResponse(content={"message": "success"})
    response.delete_cookie(key="sessionId")
    return response


class putChangeQmArg(BaseModel):
    qm: str


@app.put("/user/changeQm")
async def putChangeQmApi(item: putChangeQmArg, sessionId=Cookie(None)):
    s = session.getSession(sessionId)
    if s:
        uid = s['userId']
    else:
        return {"message": "no signIn"}
    user = db.filter("user", id=uid)
    if len(user) == 1:
        user = user[0]
    else:
        return {"message": "the id is wrong"}
    user.qm = item.qm
    user.save()
    return {"message": "success"}


class putChangePasswordArg(BaseModel):
    oldPassword: str
    newPassword: str


@app.put("/user/changePassword")
async def putChangePasswordApi(item: putChangePasswordArg, sessionId=Cookie(None)):
    s = session.getSession(sessionId)
    if s:
        uid = s["userId"]
    else:
        return {"message": "no signIn"}
    v_user = db.filter("user", id=uid)
    if len(v_user) != 1:
        return {"message": "the id is wrong"}
    user = v_user[0]
    if user.password == item.oldPassword:
        user.password = item.newPassword
        user.save()
        return {"message": "success"}
    else:
        return {"message": "the password is wrong"}


@app.get("/page/home")
async def getHomeDataApi(num: int):
    blogs = db.filterNum("blog", "time", reverse=True, num=num)
    datas = datasToArr(blogs)
    texts = []
    textDatas = db.filter("news")
    for i in textDatas:
        texts.append(i.text)
    data = {
        "message": "success",
        "sortItems": sortItems,
        "newBlogs": datas,
        "texts": texts
    }
    return data


@app.get("/page/tag")
async def getTagDataApi(tagName: str):
    blogs = db.filter("blog", tag=sortItems.index(tagName))
    datas = datasToArr(blogs)
    return {
        "message": "success",
        "blogs": datas
    }


@app.get("/page/user")
async def getUserDataApi(sessionId=Cookie(None)):
    s = session.getSession(sessionId)
    if s:
        id = s["userId"]
    else:
        return {"message": "no signIn"}
    user = db.filter("user", id=id)

    if len(user) != 0:
        user = user[0]
        blogs = db.filter("blog", user=user.id)
        blogsData = datasToArr(blogs)
        return {
            "userInfo": {
                "username": user.username,
                "nickname": user.nickname,
                "id": user.id,
                "qm": user.qm,
                "exp": user.exp,
                "k": user.k
            },
            "blogs": blogsData,
            "message": "success"
        }
    else:
        return {"message": "the id or username is wrong"}


@app.get("/page/blog")
async def getBlogDataApi(id: int):
    v_blog = db.filter("blog", id=id)
    if len(v_blog) != 1:
        return {"message": "the id is wrong"}
    blog = v_blog[0]
    d_pl = db.filter("pl", blogId=blog.id)
    pls = []
    for dp in d_pl:
        pls.append({
            "user": db.get("user", id=dp.userId).nickname,
            "date": dp.date,
            "inner": dp.inner,
            "goodNum": len(db.filter("good", plId=dp.id))
        })
    return {
        "message": "success",
        "pls": pls,
        "blog": {
            "title": blog.title,
            "inner": blog.inner,
            "id": blog.id,
            "user": db.get("user", id=blog.user).nickname,
            "date": blog.date,
            "tag": sortItems[blog.tag]
        }
    }


@app.get("/code")
async def getCodeApi(username: str, method: str = "signIn"):
    if method == "signIn" and len(db.filter("user", username=username)) == 0:
        return {"message": "username wrong"}
    global codes
    code, imgD = confirmCode.get()
    codes[username] = code.replace(" ", "")

    def delCode():
        time.sleep(60)
        if codes.get(username):
            del codes[username]
    t = threading.Thread(target=delCode)
    t.start()
    return imgD


@app.post("/edit/uploadImg")
async def postUploadImgApi(sessionId=Cookie(None), img: UploadFile = File(None)):
    s = session.getSession(sessionId)
    if s:
        user = db.get("user", id=s['userId'])
    else:
        return {"message": "no signIn"}
    data = img.file.read()
    imgId = db.create("files", file=database.sqlite3.Binary(
        data), userId=user.id).id
    url = f"/api/asset/img/{imgId}"
    return {
        "message": "success",
        "url": url
    }


@app.post("/edit/deleteImg")
async def postDelImgApi(imgId: int, sessionId=Cookie(None)):
    s = session.getSession(sessionId)
    if s:
        user = db.get("user", id=s['userId'])
    else:
        return {"message": "no signIn"}
    imgs = db.filter("files", id=imgId)
    if len(imgs) == 1:
        img = imgs[0]
        if img.userId == user.id:
            db.remove("files", id=imgId)
        else:
            return {"message": "403"}


@app.get("/asset/img/{imgId}")
async def getImgApi(imgId: int):
    img = db.get("files", id=imgId)
    imgD = img.file
    buffer = io.BytesIO(imgD)
    r = StreamingResponse(buffer)
    return r


if __name__ == "__main__":
    uvicorn.run(app)
