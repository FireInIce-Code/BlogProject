import base64
import requests
import json
d1=requests.get("http://127.0.0.1:8000/code?username=fireinice").content
d2=base64.b64decode(d1)
with open("code.png",'wb') as f:
    f.write(d2)
with open("code.txt","wb") as f:
    f.write(d1)
