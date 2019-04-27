import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
}

# 

# 使用session发送post请求，cookie保存在其中
# 在使用session进行请求登陆之后才能访问的地址
r = requests.get('https://passport.csdn.net/v1/register/pc/login/doLogin', headers=headers)

# 保存页面
with open("CSDN.html", "w", encoding="utf-8") as f:
    f.write(r.content.decode())
