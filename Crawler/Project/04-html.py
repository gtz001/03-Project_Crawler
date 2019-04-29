import re
from urllib import request, parse


class Spider():
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.baseurl = 'https://tj.lianjia.com/zufang'
        self.headers = {
            "User-Agent": """Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 
            (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"""}

    def get_page(self, url):
        req = request.Request(url)
        res = request.urlopen(req)
        html = res.read().decode()
        return html

    def parse_page(self):
        pass

    def write_parse_page(self):
        pass

    def write_page(self, basefilename, html, page):
        with open((basefilename + 'html').format(page), 'w') as f:
            f.write(html)
            f.flush()

    def main(self):
        begin = int(self.begin)
        end = int(self.end)
        basefilename = './Web/链家第{}页.'
        for page in range(begin, end + 1):
            url = self.baseurl + '/pg' + str(page + 1)
            html = self.get_page(url)
            self.write_page(basefilename, html, page + 1)


if __name__ == '__main__':
    spider = Spider()
    spider.main(2, 5)
