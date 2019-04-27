import requests

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}

data = {
    "query": "hola",
"from": "en",
"to": "zh",
"token": "3790f563a5bca02b094755033afbf138",
"sign": "372549.85108"}

post_url = "https://fanyi.baidu.com/basetrans"

r = requests.post(post_url, data=data, headers=headers)

print(r.content.decode())