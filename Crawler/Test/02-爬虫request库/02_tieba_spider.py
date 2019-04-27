import requests
import time
import os

class WebSipder:
    def __init__(self, web_name):
        self.web_name = web_name
        self.url_temp = "https://tj.lianjia.com/zufang/pg{}/#contentList"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}

    def get_url_list(self):
        url_list = []
        for i in range(5):
            url_list.append(self.url_temp.format(i))
        return url_list

    def prase_url(self, url):
        print(url)
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def save_html(self, html_str, page_num):
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        filename = "{}-第{}页.html".format(self.web_name, page_num)
        file_path = BASE_PATH +'/Web/'+ filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_str)

    def run(self):
        url_list = self.get_url_list()

        for url in url_list:
            time.sleep(10)
            html_str = self.prase_url(url)
            page_num = url_list.index(url)
            self.save_html(html_str, page_num)


if __name__ == "__main__":
    tieba_spider = WebSipder("链家")
    tieba_spider.run()
