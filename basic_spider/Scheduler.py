# coding:utf-8

from basic_spider.HtmlParse import HtmlParse
from basic_spider.HtmlDownloader import HtmlDownloader
from basic_spider.DataOutput import DataOutput
from basic_spider.URLManager import UrlManager


class Scheduler(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parse = HtmlParse()
        self.output = DataOutput()

    def crawl(self, root_url):
        self.manager.add_new_url(root_url)
        while self.manager.has_new_urls() and self.manager.used_urls_size() < 100:
            try:
                new_url = self.manager.get_new_url()
                html_page = self.downloader.download(new_url)
                new_urls, data = self.parse.parse(new_url, html_page)
                self.manager.add_new_urls(new_urls)
                self.output.store_data(data)
                print('已抓取%s个链接' % self.manager.used_urls_size())
            except Exception:
                print('crawl failed.')
        self.output.output_html()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.crawl('https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711?fr=aladdin')