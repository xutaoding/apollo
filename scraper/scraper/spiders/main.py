# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings

class MainSpider(scrapy.Spider):
    name = 'main'

    def __init__(self, url, save_path, **kwargs):
        self.url = url
        self.save_path= save_path
        self.request_body = kwargs.pop('data', None)
        self.request_method = kwargs.pop('method', 'GET')
        self.request_headers = kwargs.pop('headers', None)

        super(MainSpider, self).__init__(**kwargs)

    def start_requests(self):
        headers = settings['DEFAULT_REQUEST_HEADERS'].copy()
        headers.update(self.request_headers or {})

        yield scrapy.Request(
            self.url, method=self.request_method,
            headers=headers, body=self.request_body
        )

    def parse(self, response):
        with open(self.save_path, 'wb') as fp:
            fp.write(response.body)


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    _url = 'http://finance.sina.com.cn/roll/2017-10-27/doc-ifynfrfm9450359.shtml'
    _save_path = '/data/aegis_files/ifynfrfm9450359.html'

    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(MainSpider, url=_url, save_path=_save_path)
    crawler.start()
