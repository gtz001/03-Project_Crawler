from urllib import request
import re
import requests

from lxml import etree
import time
from multiprocessing import Queue
from threading import Thread


class XinhuaSpider(object):
    def __init__(self):
        self.baseUrl = "http://www.xinhuanet.com/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.urlQueue = Queue()
        self.parseQueue = Queue()
        self.list = []

    # URL入队列
    def getUrl(self):
        print('进入getUrl')
        res = requests.get(self.baseUrl, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        # print(html)
        parseHtml = etree.HTML(html)
        yList = parseHtml.xpath("//div[@class='part2L']//a/@href")
        for yurl in yList:
            # print(yurl)
            self.urlQueue.put(yurl)

    # get获取URL,发请求,把响应入解析队列
    def getHtml(self):
        while True:
            # 如果队列不为空
            if not self.urlQueue.empty():
                url = self.urlQueue.get()
                # 三步走
                res = requests.get(url, headers=self.headers)
                res.encoding = 'utf-8'
                html = res.text
                # print(html)
                # 放到解析队列
                tup_html = (html, url)
                self.parseQueue.put(tup_html)
            else:
                break

    # get获取html,提取并保存数据
    def parseHtml(self):
        while True:
            try:
                tup_html = self.parseQueue.get(block=True, timeout=2)# 每过两秒就从队列中取出一个
                html = tup_html[0]
                url = tup_html[1]
                print(url)

                # 获取图片连接的前半部分img_headurl，后面用来拼接
                img_headurl_rob = re.compile('(.*/\d{2}/)', re.S)
                img_headurlList = img_headurl_rob.findall(url)
                if img_headurlList:
                    # print('已找到img_headurlList')
                    img_headurl = img_headurlList[0]
                else:
                    # print('未找到img_headurlList')
                    continue

                # print(img_headurl)

                parseHtml = etree.HTML(html)

                # 获取新闻标题，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                title = parseHtml.xpath('//div[@class="h-title"]/text()')
                if not title:
                    continue
                else:
                    title = title[0]

                # print(title)
                # 获取新闻时间，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                dateList = parseHtml.xpath('//span[@class="h-time"]/text()')
                if dateList:
                    date = dateList[0]
                else:
                    continue
                # print(date)

                # 获取原新闻html，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                if '<video' in html:
                    content_rob = re.compile('<video.*</p>', re.S)

                else:
                    content_rob = re.compile('<p.*</p>', re.S)

                contentList = content_rob.findall(html)

                if contentList:
                    # print('已找到contentList')
                    content = contentList[0]

                    # print(content)
                else:
                    # print('未找到contentList')
                    continue

                # 获取首页新闻展示内容，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                firstcontentList = parseHtml.xpath('//p/text()')
                if firstcontentList:
                    firstcontent = firstcontentList[0]
                    # print(firstcontent)
                else:
                    continue

                # 图片链接进行修改
                print('图片链接进行修改')
                old_imgsrcRE = re.compile('<img.*?src="(.*?)"', re.S)
                old_imgsrcList = old_imgsrcRE.findall(content)
                for old_imgsrc in old_imgsrcList:
                    newsec = img_headurl + old_imgsrc
                    content = content.replace(old_imgsrc, newsec)

                # print(old_imgsrcList)

                d = {}

                d['title'] = title
                d['datetime'] = date
                d['firstcontent'] = firstcontent
                # d['firstimage'] = firstimage
                d['source'] = '新华网'
                d['content'] = content
                d['classes'] = '要闻'
                # print(title)
                self.list.append(d)
            except:
                break
        del d, title, date, firstcontent, content, html, parseHtml

    # 主函数
    def workOn(self):
        start = time.time()
        # URL入队列
        self.getUrl()
        # 存放所有线程列表
        tList = []
        # 采集线程开始执行
        for i in range(5):
            t = Thread(target=self.getHtml)
            tList.append(t)
            t.start()

        # 所有解析线程开始执行
        for i in range(5):
            t = Thread(target=self.parseHtml)
            tList.append(t)
            t.start()

        # # 阻塞等待回收所有线程
        for j in tList:
            j.join(timeout=2)
        end = time.time()
        print('XinhuaSpider共执行了%f秒' % (end - start))


class KuaiTechSpider(object):
    def __init__(self):
        self.url = "https://www.mydrivers.com/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.list = []

    def get_html(self, url):

        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        # print(html)
        self.get_page(html)

    def get_page(self, html):
        parseHtml = etree.HTML(html)
        pagerlList = parseHtml.xpath("//div[@class='news_info1']/ul/li/span/a/@href")
        # print(pagerlList)
        title = parseHtml.xpath("//div[@class='news_info1']/ul/li/span/a/text()")
        # print('title_',title)
        # for i in pagerlList:
        #     print(i)
        self.get_text(pagerlList)

    def get_text(self, pagerlList):
        allTitle = []
        for page in pagerlList:
            d = {}

            # 得到网页源码
            res = requests.get(page, headers=self.headers)
            res.encoding = 'utf-8'
            html = res.text
            with open('/home/tarena/html.txt', 'w') as f:
                f.write(html)
            # print(html)

            # 使用xpath得到xpath对象
            parseHtml = etree.HTML(html)

            # 得到新闻标题列表,没有匹配到时进行下一个新闻
            titlelist = parseHtml.xpath('//div[@class="news_bt"]/text()')
            if titlelist:
                title = titlelist[0]
                if title in allTitle:
                    with open('/home/tarena/title.txt', 'a') as f:
                        f.write(str(title))
                    continue
                allTitle.append(title)
            else:
                continue
            # print('title=', title)
            # 判断新闻标题是否为没有乱码的标题
            isTitle = False
            for u in title:
                if '\u4e00' <= u <= '\u9fff':
                    isTitle = True
            # 当标题符合的时候，继续获取其他信息，否则放弃此新闻，开始下一个新闻
            if not isTitle:
                continue

            # 得到时间
            dateList = parseHtml.xpath('//div[@class="news_bt1_left"]/text()')[0].strip()
            date = dateList.split('\xa0\xa0')[0]
            if date[0].isdigit() == False:
                continue
            # print('date=', date)

            # # 得到新闻内容列表
            # content = parseHtml.xpath('//div[@class="news_info"]/p/text()')
            # 匹配出原页面的内容html
            one = re.compile(
                '''<div class="news_info" style="padding-top:0px; padding-bottom:0px;">(.*?)<div  style="overflow:hidden;">'''
                , re.S)
            text = one.findall(html)

            if text:
                text = text[0]

                text = re.sub(r'src="', 'src="https:', text)

            else:
                continue

            # 获取新闻的首页展示文字
            parseFirstcontent = etree.HTML(text)
            firstcontentList = parseFirstcontent.xpath('//p/text()|//strong/text()')
            firstcontent = ''
            for fc in firstcontentList:
                firstcontent += fc
                if len(firstcontent) > 100:
                    break

            # 得到新闻来源
            source = parseHtml.xpath("//div[@class='news_bt1_left']/a[not(@class='newstiao4')]/text()")
            # 得到新闻来源链接
            if not source:
                source = '快科技'
                source_url = page
            else:
                source = source[0]
                source_url = parseHtml.xpath("//div[@class='news_bt1_left']/a/@href")[0]

            # print('source=', source)
            # print('source_url=', source_url)
            # print()
            # print(content)
            # print(text)

            # # 获取新闻页面中的图片列表
            # imgList = parseHtml.xpath('//div[@class="news_info"]/p/a/img/@src')
            # img = ''
            # # print('imgList=',imgList)
            # # 将每一张图片进行处理,保存
            # is_Firstimage = True
            # if imgList:
            # #     HaveImg = False
            # #     HaveImg = True
            #     for imgurl in imgList:
            #
            #         # print('Urldate=',Urldate)
            #         imgname = imgurl.replace('//img1.mydrivers.com/img/%s/'%Urldate,'')
            #
            #         imghttp = 'http:' + imgurl
            #         # print(imgname)
            #         # print('imghttp=',imghttp)
            #         imgres = requests.get(imghttp, headers=self.headers)
            #         imgres.encoding = 'utf-8'
            #         imghtml = imgres.content
            #
            #         imgfile = '/home/tarena/zh/毕业项目/mojian0314/static/images/newsimg/kuaikejiimg/%s' %imgname
            #
            #         # img += '/static/images/newsimg/kuaikejiimg/%s;' % imgurl[-10:]
            #
            #         if imghtml :
            #
            #             with open(imgfile, 'wb') as f:
            #                 f.write(imghtml)
            #             if is_Firstimage:
            #                 firstimage = '/static/images/newsimg/kuaikejiimg/%s'%imgname
            #                 is_Firstimage = False
            # else:
            #     continue

            # print(text)
            # print(title)

            if dateList and text:
                # d['image'] = img
                # print(firstimage)
                d['firstcontent'] = firstcontent
                # print(firstcontent)
                # d['firstimage'] = firstimage
                # print(text)
                d['title'] = title
                # print(title)
                d['datetime'] = date
                d['content'] = text
                d['source'] = source
                d['source_url'] = source_url
                d['classes'] = '科技'
                self.list.append(d)
                # print(text[0])

                if len(self.list) == 50:
                    del d
                    break

    def workOn(self):
        self.get_html(self.url)


class TiyuSpider(object):
    def __init__(self):
        self.baseUrl = "http://sports.sina.com.cn/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.urlQueue = Queue()
        self.parseQueue = Queue()
        self.list = []

    # URL入队列
    def getUrl(self):
        res = requests.get(self.baseUrl, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        parseHtml = etree.HTML(html)
        pageList = parseHtml.xpath('//*[@id="ty-top-ent0"]/div/div/ul/li/a/@href')
        pagecount = 0
        for pageurl in pageList:
            if '.shtml' in pageurl and '/doc' in pageurl:
                pagecount += 1
                pageurl = 'http:' + pageurl
                # print(pageurl)
                self.urlQueue.put(pageurl)
        print('获取%d个页面' % pagecount)

    # get获取URL,发请求,把响应入解析队列
    def getHtml(self):
        while True:
            # 如果队列不为空
            if not self.urlQueue.empty():
                url = self.urlQueue.get()
                # print(url)

                # 获取新闻页原html放到解析队列
                res = requests.get(url, headers=self.headers)
                res.encoding = 'utf-8'
                html = res.text
                # print(html)
                # 放到解析队列
                self.parseQueue.put(html)
            else:
                print('html全部放到解析队列')
                break

    # get获取html,提取并保存数据
    def parseHtml(self):
        html_count = 0
        while True:
            try:
                html = self.parseQueue.get(block=True, timeout=20)

                print('从队列得到html')
                html_count += 1
                parseHtml = etree.HTML(html)

                # print('parseHtml中html',html)
                # break
                # 获取原新闻html，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                p = re.compile(
                    '.*<div class="article" id="artibody" data-sudaclick="blk_content">(.*)<div id="left_hzh_ad">.*',
                    re.S)
                print('开始得到content')
                content = p.findall(html)
                if content:
                    content = content[0]
                else:
                    print('未取得content')
                    continue
                # print(content)

                # 获取新闻标题，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                title = parseHtml.xpath('/html/body/div/h1/text()')

                if not title:
                    print('未取得title')
                    continue
                else:
                    title = title[0]
                # print(title)

                # 获取新闻来源，如果没有获取到，则跳过此新闻，进行下一个新闻获取

                source = parseHtml.xpath('//*[@id="top_bar"]/div/div[2]/a/text()')
                if not source:
                    continue
                else:
                    source = source[0]
                # print(source)

                # 获取首页新闻展示内容，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                firstcontent = ''.join(parseHtml.xpath('//*[@id="artibody"]/p/text()'))
                if not firstcontent:
                    continue
                else:
                    firstcontent = firstcontent[:101]
                # print(firstcontent)

                # 获取新闻时间，如果没有获取到，则跳过此新闻，进行下一个新闻获取

                date = parseHtml.xpath('//*[@id="top_bar"]/div/div[2]/span/text()')
                # ltime = re.findall('(\d{4}).*?(\d{2}).*?(\d{2}).*?(\d{2}):(\d{2}).*?', date[0])
                if not date:
                    continue
                else:
                    ltime = re.findall('(\d{4}).*?(\d{2}).*?(\d{2}).*?(\d{2}):(\d{2})', date[0])
                    r = ltime[0]
                    datetime = r[0] + '-' + r[1] + '-' + r[2] + ' ' + r[3] + ':' + r[4]
                # print(datetime)

                # 获取页面首页展示firstimage
                img = parseHtml.xpath('//*[@id="artibody"]/div[1]/img/@src')

                if img:
                    firstimage = 'http:' + img[0]
                else:
                    firstimage = ''
                # print(firstimage)

                # 将获取的新闻信息存到字典中，在把字典加入到列表里
                d = {}

                d['title'] = title
                d['datetime'] = datetime
                d['firstcontent'] = firstcontent
                d['firstimage'] = firstimage
                d['source'] = source
                d['content'] = content
                # print(content)
                d['classes'] = '体育'
                # print(title)
                # print(d)
                self.list.append(d)
            except Exception as e:
                print('错误为', e)
                break

                # except:
                #     print('结束循环')

        try:
            del d, title, datetime, firstcontent, firstimage, source, content, html, parseHtml
        except UnboundLocalError:
            pass
        print('共获取%d个html' % html_count)

    # 主函数
    def workOn(self):
        start = time.time()
        # URL入队列
        self.getUrl()
        # 存放所有线程列表
        tList = []
        # 采集线程开始执行
        for i in range(10):
            t = Thread(target=self.getHtml)
            tList.append(t)
            t.start()

        # 所有解析线程开始执行
        for i in range(10):
            t = Thread(target=self.parseHtml)
            tList.append(t)
            t.start()

        # 阻塞等待回收所有线程
        for j in tList:
            j.join()
        end = time.time()
        print('TiyuSpider共执行了%f秒' % (end - start))


class CsdnSpider(object):
    def __init__(self):
        self.baseUrl = "https://www.csdn.net/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.urlQueue = Queue()
        self.parseQueue = Queue()
        self.list = []

    # URL入队列
    def getUrl(self):
        res = requests.get(self.baseUrl, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        # print(html)
        parseHtml = etree.HTML(html)
        pageList = parseHtml.xpath("//ul[@class='feedlist_mod home']/li//div[@class='title']/h2/a/@href")
        # print()
        for pageurl in pageList:
            # print(pageurl)
            self.urlQueue.put(pageurl)

    # get获取URL,发请求,把响应入解析队列
    def getHtml(self):
        while True:
            # 如果队列不为空
            if not self.urlQueue.empty():
                url = self.urlQueue.get()
                # 三步走
                res = requests.get(url, headers=self.headers)
                res.encoding = 'utf-8'
                html = res.text
                # print(html)
                # 放到解析队列
                self.parseQueue.put(html)
            else:
                break

    # get获取html,提取并保存数据
    def parseHtml(self):
        allTitle = []
        while True:
            try:
                html = self.parseQueue.get(block=True, timeout=2)
                parseHtml = etree.HTML(html)

                # 获取新闻标题，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                title = parseHtml.xpath("//h1[@class='title-article']/text()")
                if title:
                    title = title[0]
                    if title in allTitle:
                        print('下一个新闻')
                        continue
                    else:
                        allTitle.append(title)
                else:
                    print('下一个新闻')
                    continue
                # print(title)

                # 得到新闻来源
                source = 'csdn'
                # print(source)

                # 得到新闻来源链接
                source_url = self.baseUrl
                # print(source_url)

                # 获取原新闻html，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                one = re.compile('''<article class="baidu_pl">(.*?)</article>''', re.S)
                content = one.findall(html)
                # print(content)
                if content:
                    content = content[0]
                else:
                    continue
                # print(content)

                # 获取新闻的首页展示文字
                parseFirstcontent = etree.HTML(content)
                firstcontentList = parseFirstcontent.xpath(
                    '//div[@class="htmledit_views"]/p/text() |  //div[@class="htmledit_views"]//li/text()| //div[@class="htmledit_views"]//strong/text()')
                # print(firstcontentList)

                firstcontent = ''
                for fc in firstcontentList:
                    firstcontent += fc
                    if len(firstcontent) > 100:
                        break
                # print(firstcontent)
                # print(firstcontent)

                # 获取新闻时间，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                dateList = parseHtml.xpath("//span[@class='time']/text()")[0].strip()
                # print(dateList)
                if dateList:
                    date = ''
                    dt_num = 0
                    # 将得到的时间调整为数据库可以识别的格式
                    for dt in dateList:
                        if dt in ['年', '月', '日']:

                            dt_num += 1
                            dt = '-'
                            if dt_num > 2:
                                continue
                        date += dt
                else:
                    continue
                # print(date)

                # 将获取的新闻信息存到字典中，在把字典加入到列表里
                d = {}

                d['title'] = title
                d['datetime'] = date
                d['firstcontent'] = firstcontent
                d['source_url'] = source_url
                d['source'] = source
                d['content'] = content
                d['classes'] = 'IT'
                print(title)
                self.list.append(d)
            except:
                break
        try:
            del d, title, date, firstcontent, source, content, html, parseHtml
        except UnboundLocalError:
            pass

    # 主函数
    def workOn(self):
        start = time.time()
        # URL入队列
        self.getUrl()
        # 存放所有线程列表
        tList = []
        # 采集线程开始执行
        for i in range(5):
            t = Thread(target=self.getHtml)
            tList.append(t)
            t.start()

        # 所有解析线程开始执行
        for i in range(5):
            t = Thread(target=self.parseHtml)
            tList.append(t)
            t.start()

        # 阻塞等待回收所有线程
        for j in tList:
            j.join()
        end = time.time()
        print('Yulespider共执行了%f秒' % (end - start))


class Caijingspider(object):
    def __init__(self):
        self.baseUrl = 'https://finance.sina.com.cn/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.urlQueue = Queue()
        self.parseQueue = Queue()
        self.list = []

    # URL入队列
    def getUrl(self):
        res = requests.get(self.baseUrl, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        parseHtml = etree.HTML(html)
        pageList = parseHtml.xpath('//*[@id="fin_tabs0_c0"]/div[2]//a/@href')
        for pageurl in pageList:
            # print(pageurl)
            self.urlQueue.put(pageurl)

    # get获取URL,发请求,把响应入解析队列
    def getHtml(self):
        while True:
            # 如果队列不为空
            if not self.urlQueue.empty():
                url = self.urlQueue.get()
                # 三步走
                res = requests.get(url, headers=self.headers)
                res.encoding = 'utf-8'
                html = res.text
                # print(html)
                # 放到解析队列
                self.parseQueue.put(html)
            else:
                break

    # get获取html,提取并保存数据
    def parseHtml(self):
        while True:
            try:
                html = self.parseQueue.get(block=True, timeout=8)
                p = re.compile('.*<!-- 原始正文begin -->(.*)<!-- 编辑姓名及工作代码-->.*', re.S)
                html0 = p.findall(str(html))

                if html0:

                    # 获取原新闻html，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                    content = html0[0] + "</div>"
                    parseHtml = etree.HTML(html)

                    # 获取新闻标题，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                    title = parseHtml.xpath('//*[@class="main-title"]/text()')
                    # print('title=',title)

                    if not title:
                        continue
                    else:
                        title = title[0]

                    # 获取新闻来源，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                    source = parseHtml.xpath(
                        '//*[@id="top_bar"]/div/div[2]/a/text() | //*[@id="top_bar"]/div/div[2]/span[2]/text()')
                    if not source:
                        continue
                    else:
                        source = source[0]
                    # print(source)

                    # 获取首页新闻展示内容，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                    firstcontent = ''.join(parseHtml.xpath('//*[@id="artibody"]/p/text()'))
                    if not firstcontent:
                        continue
                    else:
                        firstcontent = firstcontent[:101]

                    # 获取新闻时间，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                    date = parseHtml.xpath('//*[@id="top_bar"]/div/div[2]/span[1]/text()')
                    # ltime = re.findall('(\d{4}).*?(\d{2}).*?(\d{2}).*?(\d{2}):(\d{2}).*?', date[0])
                    if not date:
                        continue
                    else:
                        ltime = re.findall('(\d{4}).*?(\d{2}).*?(\d{2}).*?(\d{2}):(\d{2})', date[0])
                        r = ltime[0]
                        datetime = r[0] + '-' + r[1] + '-' + r[2] + ' ' + r[3] + ':' + r[4]

                    # 获取页面首页展示firstimage
                    img = parseHtml.xpath('//*[@class="img_wrapper"]/img/@src')
                    if img:
                        firstimage = 'http:' + img[0]
                    else:
                        firstimage = ''
                    # print(firstimage)

                    # 将获取的新闻信息存到字典中，在把字典加入到列表里
                    d = {}

                    d['title'] = title
                    d['datetime'] = datetime
                    d['firstcontent'] = firstcontent
                    d['firstimage'] = firstimage
                    d['source'] = source
                    d['content'] = content
                    d['classes'] = '财经'
                    # print(title)
                    self.list.append(d)
                else:
                    continue
            except:
                break
        try:
            del d, title, datetime, firstcontent, firstimage, source, content, html, parseHtml
        except UnboundLocalError:
            pass

    # 主函数
    def workOn(self):
        start = time.time()
        # URL入队列
        self.getUrl()
        # 存放所有线程列表
        tList = []
        # 采集线程开始执行
        for i in range(5):
            t = Thread(target=self.getHtml)
            tList.append(t)
            t.start()

        # 所有解析线程开始执行
        for i in range(5):
            t = Thread(target=self.parseHtml)
            tList.append(t)
            t.start()

        # 阻塞等待回收所有线程
        for j in tList:
            j.join()
        end = time.time()
        print('Caijingspider共执行了%f秒' % (end - start))


class JunshiSpider(object):
    def __init__(self):
        self.baseUrl = "https://mil.news.sina.com.cn/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.urlQueue = Queue()
        self.parseQueue = Queue()
        self.list = []

    # URL入队列
    def getUrl(self):
        res = requests.get(self.baseUrl, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        parseHtml = etree.HTML(html)
        pageList = parseHtml.xpath(
            '//ul[@class="part1 arcticle-list"]/li/a/@href | //ul[@class="part2 arcticle-list"]/li/a/@href')
        for pageurl in pageList:
            # print(pageurl)
            self.urlQueue.put(pageurl)

    # get获取URL,发请求,把响应入解析队列
    def getHtml(self):
        while True:
            # 如果队列不为空
            if not self.urlQueue.empty():
                url = self.urlQueue.get()
                # 三步走
                res = requests.get(url, headers=self.headers)
                res.encoding = 'utf-8'
                html = res.text
                # print(html)
                # 放到解析队列
                self.parseQueue.put(html)
            else:
                break

    # get获取html,提取并保存数据
    def parseHtml(self):
        while True:
            try:
                html = self.parseQueue.get(block=True, timeout=8)
                parseHtml = etree.HTML(html)
                # print(html)

                # 获取新闻标题，没有获取到则跳过，进行下一条新闻获取
                title = parseHtml.xpath('//div[@class="second-title"]/text()')
                if not title:
                    return
                else:
                    title = title[0]
                # print(title)

                # 获取新闻来源，没有获取到则跳过，进行下一条新闻获取
                source = parseHtml.xpath(
                    '//*[@id="top_bar"]/div/div[2]/a/text() | //*[@id="top_bar"]/div/div[2]/span[2]/text()')
                if not source:
                    return
                else:
                    source = source[0]
                # print(source)

                # 获取首页展示文本，没有获取到则跳过，进行下一条新闻获取
                firstcontent = ''.join(parseHtml.xpath('//*[@id="article"]//p/text()'))
                if not firstcontent:
                    return
                else:
                    firstcontent = firstcontent[:101]
                # print(firstcontent)

                # 获取新闻时间，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                date = parseHtml.xpath('//*[@id="top_bar"]/div/div[2]/span/text()')
                if date:
                    ltime = re.findall('(\d{4}).*?(\d{2}).*?(\d{2}).*?(\d{2}):(\d{2})', date[0])
                    if not ltime:
                        continue
                    else:
                        r = ltime[0]
                        datetime = r[0] + '-' + r[1] + '-' + r[2] + ' ' + r[3] + ':' + r[4]
                else:
                    continue
                # print(datetime)

                # 获取新闻的原html，没有获取到则跳过，进行下一条新闻获取
                p = re.compile('''.*<!-- 正文 start -->(.*)<div class="article-bottom clearfix" id='article-bottom'>.*''',
                               re.S)
                content = p.findall(html)
                if not content:
                    return
                else:
                    content = content[0]
                # print(content)

                # 获取新闻的首页图片firstimage，没有获取到则为空
                img = parseHtml.xpath('//*[@class="img_wrapper"]/img/@src')
                if img:
                    firstimage = 'http:' + img[0]
                else:
                    firstimage = ''

                print(firstimage)
                # 将获取的新闻信息存到字典中，在把字典加入到列表里
                d = {}

                d['title'] = title
                d['datetime'] = datetime
                d['firstcontent'] = firstcontent
                d['firstimage'] = firstimage
                d['source'] = source
                d['content'] = content
                d['classes'] = '军事'
                # print(title)
                self.list.append(d)
            except:
                break
        try:
            del d, title, datetime, firstcontent, firstimage, source, content, html, parseHtml
        except UnboundLocalError:
            pass

    # 主函数
    def workOn(self):
        start = time.time()
        # URL入队列
        self.getUrl()
        # 存放所有线程列表
        tList = []
        # 采集线程开始执行
        for i in range(10):
            t = Thread(target=self.getHtml)
            tList.append(t)
            t.start()

        # 所有解析线程开始执行
        for i in range(10):
            t = Thread(target=self.parseHtml)
            tList.append(t)
            t.start()

        # 阻塞等待回收所有线程
        for j in tList:
            j.join()
        end = time.time()
        print('JunshiSpider共执行了%f秒' % (end - start))


class Yulespider(object):
    def __init__(self):
        self.baseUrl = 'http://www.dzyule.com/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.urlQueue = Queue()
        self.parseQueue = Queue()
        self.list = []

    # URL入队列
    def getUrl(self):
        res = requests.get(self.baseUrl, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        parseHtml = etree.HTML(html)
        yList = parseHtml.xpath('//*[@class="pfl-l"]//a/@href')
        for yurl in yList:
            # print(yurl)
            self.urlQueue.put(yurl)

    # get获取URL,发请求,把响应入解析队列
    def getHtml(self):
        while True:
            # 如果队列不为空
            if not self.urlQueue.empty():
                url = self.urlQueue.get()
                # 三步走
                res = requests.get(url, headers=self.headers)
                res.encoding = 'gbk'
                html = res.text
                # 放到解析队列
                self.parseQueue.put(html)
            else:
                break

    # get获取html,提取并保存数据
    def parseHtml(self):
        while True:
            try:
                html = self.parseQueue.get(block=True, timeout=2)
                parseHtml = etree.HTML(html)

                # 获取新闻标题，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                title = parseHtml.xpath('//*[@id="main"]/div[1]/div[2]/div[1]/h1/text()')
                if not title:
                    continue
                else:
                    title = title[0]

                # 获取新闻来源，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                source = parseHtml.xpath('//*[@id="main"]/div[1]/div[2]/div[1]/div[1]/span[2]/a/text()')
                if not source:
                    continue
                else:
                    source = source[0]

                # 获取首页新闻展示内容，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                firstcontent = ''.join(parseHtml.xpath('//*[@id="main"]/div[1]/div[2]/div[1]/div[2]/p/text()'))
                if not firstcontent:
                    continue
                else:
                    firstcontent = firstcontent[:101]

                # 获取新闻时间，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                date = parseHtml.xpath('//*[@id="main"]/div[1]/div[2]/div[1]/div[1]/span[1]/text()')
                ltime = re.findall('(\d{4}).*?(\d{2}).*?(\d{2}).*?(\d{2}):(\d{2}).*?', date[0])
                if not ltime:
                    continue
                else:
                    r = ltime[0]
                    datetime = r[0] + '-' + r[1] + '-' + r[2] + ' ' + r[3] + ':' + r[4]

                # 获取原新闻html，如果没有获取到，则跳过此新闻，进行下一个新闻获取
                p = re.compile(
                    '.*<div class="text" style="margin-top: 9px;">(.*)</div>.*?<div style="text-align:center;margin-top:10px;">.*',
                    re.S)
                content = p.findall(str(html))
                if not content:
                    continue
                else:
                    content = content[0]

                img = parseHtml.xpath('//*[@class="text"]/center[1]/img/@src')
                if img:
                    firstimage = img[0]
                else:
                    firstimage = ''

                # 将获取的新闻信息存到字典中，在把字典加入到列表里
                d = {}

                d['title'] = title
                d['datetime'] = datetime
                d['firstcontent'] = firstcontent
                d['firstimage'] = firstimage
                d['source'] = source
                d['content'] = content
                d['classes'] = '娱乐'
                # print(title)
                self.list.append(d)
            except:
                break
        try:
            del d, title, datetime, firstcontent, firstimage, source, content, html, parseHtml
        except UnboundLocalError:
            pass

    # 主函数
    def workOn(self):
        start = time.time()
        # URL入队列
        self.getUrl()
        # 存放所有线程列表
        tList = []
        # 采集线程开始执行
        for i in range(5):
            t = Thread(target=self.getHtml)
            tList.append(t)
            t.start()

        # 所有解析线程开始执行
        for i in range(5):
            t = Thread(target=self.parseHtml)
            tList.append(t)
            t.start()

        # 阻塞等待回收所有线程
        for j in tList:
            j.join()
        end = time.time()
        print('Yulespider共执行了%f秒' % (end - start))


if __name__ == "__main__":
    spider = XinhuaSpider()
    spider.workOn()

    spider = KuaiTechSpider()
    spider.workOn()
