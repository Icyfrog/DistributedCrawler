from bs4 import BeautifulSoup
import urllib
import urllib.request
import time
import json
import os


class MySpider():
    name = "spider"

    def __init__(self):

        # self.file = open('./test/demo1_quotes_bs.json', 'w');
        self.file = open('demo1_quotes_bs.json', 'w');
        # 设置待爬取网站列表
        self.urls = []
        for i in range(1, 3):
            self.urls.append('http://quotes.toscrape.com/page/' + str(i))

        #       初始化效果 效果等同
        #         self.urls = [
        #             'http://quotes.toscrape.com/page/1/',
        #             'http://quotes.toscrape.com/page/2/',
        #         ]

        # 设置header
        self.headers = {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'}

        print(self.urls)

    # 利用urllib获取网站的html，并导入BeautifulSoup
    def bs_request(self, url):
        request = urllib.request.Request(url, headers=self.headers)
        html = urllib.request.urlopen(request).read()
        response = BeautifulSoup(html, 'html.parser')
        self.parse(url, response)

    # start函数，调用此函数可开始爬虫
    def start(self):
        for url in self.urls:
            self.bs_request(url)

    # parse方法用于解析html文件
    def parse(self, url, response):

        # 提取名言列表
        quotes = response.find_all("div", class_="quote")
        for quote in quotes:
            # 提取每条名言中的作者名
            author = quote.find("small", class_="author").get_text()
            # 提取名言的文字内容
            text = quote.find(class_="text").get_text()
            # 提取名言标签
            tags = [t.get_text() for t in quote.select(".tags .tag")]
            # 构建字典对象
            item = {"author": author, "text": text, "tags": tags}
            # 将字典转换成json字符串
            line = json.dumps(dict(item))
            # 将每个条目写入文件
            self.file.write(line + "\n")
        # 及时将内容写入文件，否则可能会出现少许延迟
        self.file.flush()
        os.fsync(self.file)
        # 输出当前解析完成的网页网址，可以当做爬取进度来看待,与程序逻辑无关
        print("over: " + url)


# 新建爬虫对象
spider = MySpider()

# 开始爬虫
spider.start()
