# coding: utf-8
class UrlManager(object):
    def __init__(self):
        self.new_urls = set()  # 未爬取url
        self.used_urls = set()  # 已爬取url

    # 判断是否有未爬取urls
    def has_new_urls(self):
        return self.new_urls_size() is not None

    # 获取一个未爬取url
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.used_urls.add(new_url)
        return new_url

    # 将新的url添加到new_urls里面
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.used_urls:
            self.new_urls.add(url)

    # 批量添加新url
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.new_urls.add(url)

    # 获取size
    def new_urls_size(self):
        return len(self.new_urls)

    def used_urls_size(self):
        return len(self.used_urls)