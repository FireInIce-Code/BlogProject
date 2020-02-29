import random
import base64
import io
from PIL import Image,ImageDraw,ImageFont
#验证码长度
CODELEN=4
#验证码可选码列表
CODES=list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
#字体大小
FONTSIZE=20
#生成一个随机验证码
def randomCode():
    code=""
    for i in range(CODELEN):
        code+=random.choice(CODES)+" "
    return code[:-1]

#生成一个随机的颜色
def getColor():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

#绘制干扰线
def drawLines(ctx,img):
    #获取长宽
    w,h=img.size
    #干扰线数量
    linenum=random.randint(3,6)
    for i in range(linenum):
        #起始位置,终止位置
        sx,sy=random.randint(0,20),random.randint(0,h-1)
        ex,ey=random.randint(w-20,w-1),random.randint(0,h-1)
        #用随机颜色绘制
        ctx.line((sx,sy,ex,ey),fill=getColor())

#绘制干扰点
def drawPoints(ctx,img):
    #获取长宽
    w,h=img.size
    #干扰点数量
    pointNum=random.randint(100,200)
    for i in range(pointNum):
        #随机颜色绘制
        ctx.point([random.randint(0,w),random.randint(0,h)],fill=getColor())

#根据文字生成图像
def getCode(textCode):
    #加载字体,微软雅黑
    font=ImageFont.truetype("staticAsset/simhei.ttf",FONTSIZE)
    #火气文字大小
    f_w,f_h=font.getsize(textCode)
    #计算图像大小
    size=(f_w+20,f_h+20)
    #背景颜色随机
    bgC=getColor()
    #文字颜色为背景颜色的反色
    tC=tuple([255-bgC[i] for i in range(3)])
    #创建图像
    imgCode=Image.new("RGB",size,bgC)
    ctx=ImageDraw.Draw(imgCode)
    
    #绘制文字
    ctx.text((10,10),textCode,font=font,anchor="nw",fill=tC)
    #绘制干扰点和干扰线
    drawLines(ctx,imgCode)
    drawPoints(ctx,imgCode)
    return imgCode

#将图像编码
def encodeImg(img):
    #创建内存的数据流
    buffer=io.BytesIO()
    #将图片存储到内存中
    img.save(buffer,format="JPEG")
    #再读取内存中的二进制数据
    byteData=buffer.getvalue()
    #使用base64编码
    base64str=base64.b64encode(byteData)
    #返回
    return base64str.strip(b"\"")
    
#获取一个随机验证码
def get():
    textCode=randomCode()
    return textCode,encodeImg(getCode(textCode))
