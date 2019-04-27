import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}

data = {
    "from": "en", "to": "zh", "query": "hola", "transtype": "translang", "simple_means_flag": "3",
    "sign": "372549.85108", "token": "3790f563a5bca02b094755033afbf138"}

post_url = "https://fanyi.baidu.com/v2transapi"

r = requests.post(post_url, data=data, headers=headers)

print(r.content.decode())