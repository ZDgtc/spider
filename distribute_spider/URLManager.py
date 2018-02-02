# coding:utf-8
import hashlib
import pickle


class URLManager(object):
    # 加载未爬取和已爬取的URL集合
    def __init__(self):
        self.new_urls = self.load_progress('new_urls.txt')
        self.used_urls = self.load_progress('used_urls.txt')

    # 判断是否还有未爬取的URL
    def has_new_urls(self):
        return self.new_url_size() != 0

    # 从未爬取URL集合中获取一个URL
    def get_new_url(self):
        new_url = self.new_urls.pop()
        m = hashlib.md5
        m.update(new_url)
        self.used_urls.add(m.hexdigest()[8:-8])
        return new_url

    # 向未爬取URL集合中添加一个URL
    def add_new_url(self, new_url):
        if new_url is None:
            return
        m = hashlib.md5
        m.update(new_url)
        # 验证该URL是否已存在未爬取URL集合中，以及md5摘要是否已包含在已爬取URL集合中
        if new_url not in self.new_urls and m.hexdigest()[8:-8] not in self.used_urls:
            self.new_urls.add(new_url)

    # 一次性添加多个URL
    def add_new_urls(self, new_urls):
        if new_urls is None or len(new_urls) == 0:
            return
        for url in new_urls:
            self.add_new_url(url)

    # 返回未爬取URL集合大小
    def new_url_size(self):
        return len(self.new_urls)

    # 返回已爬取URL集合大小
    def used_url_size(self):
        return len(self.used_urls)

    # 保存进度
    def save_progress(self, path, data):
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    # 加载进度
    def load_progress(self, path):
        try:
            with open(path,'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except:
            print('无进度文件，创建%s' % path)
        return set()