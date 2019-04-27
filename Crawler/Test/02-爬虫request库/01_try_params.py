import requests

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}

# p = {"wd":"传智播客"}

# url_temp = "https://www.baidu.com/s"

url_temp = "https://www.baidu.com/s?wd={}".format("传智播客")

r = requests.get(url_temp,headers=headers)

print(r.status_code)
print(r.request.url)