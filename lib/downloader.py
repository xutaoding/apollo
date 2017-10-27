# -*- coding: utf-8 -*-

import urllib2
import chardet


class Downloader(object):
    def __init__(self, url, data=None, method='GET', headers=None):
        self.url = url
        self.data = data
        self.method = method
        self._headers = headers

    @property
    def headers(self):
        default_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/61.0.3163.100 Safari/537.36'
        }

        default_headers.update(self._headers or {})

        return default_headers

    def download(self):
        if self.method == 'GET':
            req = urllib2.Request(self.url, headers=self.headers)
        elif self.method == 'POST':
            req = urllib2.Request(self.url, data=self.data, headers=self.headers)
        else:
            raise

        try:
            response = urllib2.urlopen(req, timeout=30.0)
            source_page = response.read()
            response.close()

            return self.to_utf8(source_page)
        except Exception as exe:
            return str(exe)

    @staticmethod
    def to_utf8(html):
        charset = chardet.detect(html)['encoding']
        if charset is None:
            return html
        if charset != 'utf-8' and charset == 'GB2312':
            charset = 'gb18030'

        return html.decode(charset).encode('utf-8')
