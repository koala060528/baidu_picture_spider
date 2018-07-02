import requests
import json
import os
from bs4 import BeautifulSoup
import sys
import urllib.request
import urllib.parse
import socket

timeout = 2
socket.setdefaulttimeout(timeout)


class Crawler:
    key = ''
    total = 0
    start = 0
    path = ''
    index = 0
    _headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/53'
    }

    def __init__(self, key, total, start):
        self.key = key
        self.total = total
        self.start = start
        self.index = start * 60
        # 创建存储目录
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', key)
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path

    def get_referrer(self, url):
        par = urllib.parse.urlparse(url)
        if par.scheme:
            return par.scheme + '://' + par.netloc
        else:
            return par.netloc

    def get_js(self, start, total):
        url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + self.key + '&pn=' + str(
            start * 60) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
        try:
            data = requests.get(url, headers=self._headers).content.decode('utf8')
            js = json.loads(data, strict=False)  # 不严格检查json语法
            self.get_img(js)
        except Exception as e:
            pass

        if start <= total:
            self.get_js(start + 1, self.total)

    def get_img(self, js):
        url_lis = []
        for obj in js.get('imgs'):
            url_lis.append(obj.get('objURL'))
        self.save_img(url_lis)

    def save_img(self, url_lis):
        for url in url_lis:
            file_name = url.split('/')[-1]
            name = file_name.split('.')[0]
            ext = file_name.split('.')[-1]
            if len(ext) <= 5:
                file_path = os.path.join(self.path, file_name)
                if not os.path.exists(file_path):
                    refer = self.get_referrer(url)
                    try:
                        headers = self._headers
                        headers['Referer'] = refer
                        req = urllib.request.Request(url, headers=headers)
                        img = urllib.request.urlopen(req).read()
                        print('正在保存第{0}张图片：{1}'.format(self.index, file_name))
                        open(file=file_path, mode='wb').write(img)

                    except Exception as e:
                        print('下载失败')
            else:
                print('文件名不正确')
            self.index += 1
        pass

    def start_craw(self):
        self.get_js(self.start, self.total)


if __name__ == '__main__':
    sys.setrecursionlimit(10000)  # 设置递归深度
    c = Crawler(key='自拍', total=250, start=0)
    c.start_craw()
