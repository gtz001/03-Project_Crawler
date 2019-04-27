import requests

proxies = {"http": "http://183.237.206.92:53281"}
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}

r = requests.get("http://www.baidu.com", proxies=proxies)

print(r.status_code)
