import requests

response = requests.get('https://gss3.bdstatic.com/-Po3dSag_xI4khGkpoWK1HF6hhy/baike/whfpf%3D268%2C152%2C50/sign=c8ecdfe2a81ea8d38a772744f1370278/faf2b2119313b07e3196385102d7912397dd8c44.jpg')

with open('01.jpg','wb') as f:
    f.write(response.content)