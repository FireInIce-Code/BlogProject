import base64
import requests
import json
d=requests.get("http://127.0.0.1:8000/code?username=fireinice").content
d=base64.b64decode(d)
with open("code.png",'wb') as f:
    f.write(d)

