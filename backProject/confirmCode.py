import random
import base64
import io
from PIL import Image,ImageDraw,ImageFont
CODELEN=4
CODES=list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
FONTSIZE=20
def randomCode():
    code=""
    for i in range(CODELEN):
        code+=random.choice(CODES)+" "
    return code[:-1]

def getColor():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def drawLines(ctx,img):
    w,h=img.size
    linenum=random.randint(3,6)
    for i in range(linenum):
        sx,sy=random.randint(0,20),random.randint(0,h-1)
        ex,ey=random.randint(w-20,w-1),random.randint(0,h-1)
        ctx.line((sx,sy,ex,ey),fill=getColor())

def drawPoints(ctx,img):
    w,h=img.size
    pointNum=random.randint(100,200)
    for i in range(pointNum):
        ctx.point([random.randint(0,w),random.randint(0,h)],fill=getColor())

def getCode(textCode):
    font=ImageFont.truetype("staticAsset/simhei.ttf",FONTSIZE)
    f_w,f_h=font.getsize(textCode)
    size=(f_w+20,f_h+20)
    bgC=getColor()
    tC=tuple([255-bgC[i] for i in range(3)])
    imgCode=Image.new("RGB",size,bgC)
    ctx=ImageDraw.Draw(imgCode)
    
    ctx.text((10,10),textCode,font=font,anchor="nw",fill=tC)
    drawLines(ctx,imgCode)
    drawPoints(ctx,imgCode)
    return imgCode

def encodeImg(img):
    buffer=io.BytesIO()
    img.save(buffer,format="JPEG")
    byteData=buffer.getvalue()
    base64str=base64.b64encode(byteData)
    return base64str.strip(b"\"")
    
def get():
    textCode=randomCode()
    return textCode,encodeImg(getCode(textCode))
