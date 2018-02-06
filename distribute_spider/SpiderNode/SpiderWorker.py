# coding: utf-8
from multiprocessing.managers import BaseManager
from distribute_spider.SpiderNode.HtmlParse import HtmlParse
from distribute_spider.SpiderNode.HtmlDownloader import HtmlDownloader


class SpiderWorker(object):
    def __init__(self):
        # 使用BaseManager注册获取Queue的方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        # 连接到服务器
        server_addr = '127.0.0.1'
        print('Connect to server %s...' % server_addr)
        self.m = BaseManager(address=(server_addr, 8001), authkey=b'baike')
        self.m.connect()
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParse()
        print('Init finish.')

    def crawl(self):
        while True:
            try:
                if not self.task.empty():
                    url = self.task.get()
                    if url == 'end':
                        print('爬虫节点正在停止工作')
                        self.result.put({'new_urls': 'end', 'data': 'end'})
                        return
                    print('正在解析%s' % url)
                    content = self.downloader.download(url)
                    new_urls, data = self.parser.parse(url, content)
                    print('已获取到url: %s，已获取到数据: %s' % (new_urls, data))
                    self.result.put({'new_urls': new_urls, 'data': data})
            except EOFError:
                print('控制节点连接失败')
                return
            except Exception as e:
                print(e)
                print('crawl failed')

if __name__ == '__main__':
    spider = SpiderWorker()
    spider.crawl()


