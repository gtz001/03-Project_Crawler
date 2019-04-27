import requests
import json
import sys

query_str = sys.argv[1]


headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36"
}

data = {
    "f": "auto",
    "t": "auto",
    "w": query_str
}

post_url = "http://fy.iciba.com/ajax.php?a=fy"

r = requests.post(post_url, data=data, headers=headers)

dict_ret = json.loads(r.content.decode())
ret = dict_ret['content']['out']


print(ret)
