# coding: utf-8
from multiprocessing.managers import BaseManager
from multiprocessing import Process,freeze_support,Queue
import time
from distribute_spider.ControllerNode.URLManager import URLManager
from distribute_spider.ControllerNode.DataOutput import DataOutput


class NodeManager(object):
    def start_manager(self, url_q, result_q):
        self.url_q = url_q
        self.result_q = result_q
        def get_task():
            return self.url_q
        def get_result():
            return self.result_q
        BaseManager.register('get_task_queue', callable=get_task)
        BaseManager.register('get_result_queue', callable=get_result)
        manager = BaseManager(address=('127.0.0.1', 8001), authkey=b'baike')
        return manager

    # 将url通过url_q传递到爬虫节点，将conn_q中的url存储到url管理进程
    def url_manager_proc(self, url_q, conn_q, root_url):
        url_manager = URLManager()
        url_manager.add_new_url(root_url)
        while True:
            while url_manager.has_new_urls():
                # 从url管理器获取新的url
                new_url = url_manager.get_new_url()
                # 将新url发送到工作节点
                url_q.put(new_url)
                print('The total number of used urls is %s' % url_manager.used_url_size())
                # 爬取url数量超过2000关闭进程，保存进度
                if url_manager.used_url_size() > 2000:
                    url_q.put('end')
                    print('控制节点发起结束通知...')
                    # 关闭管理节点，并存储set状态
                    url_manager.save_progress('new_urls.txt', url_manager.new_urls)
                    url_manager.save_progress('used_urls.txt', url_manager.used_urls)
                    return
            # 从conn_q获取url添加到url管理进程
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException:
                time.sleep(0.1)

    # 结果分析进程
    def result_solve_proc(self, result_q, conn_q, store_q):
        while True:
            try:
                if not result_q.empty():
                    content = result_q.get(True)
                    print('获取到返回数据：%s' % content)
                    if content['new_urls'] == 'end':
                        print('结果分析进程结束')
                        store_q.put('end')
                        return
                    # 将结果返回的urls set传递到conn_q，将返回的数据传递到store_q
                    conn_q.put(content['new_urls'])
                    store_q.put(content['data'])
                else:
                    time.sleep(0.1)
            except BaseException:
                time.sleep(0.1)

    def store_proc(self, store_q):
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print('存储进程结束')
                    output.output_end(output.filepath)
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)

if __name__ == '__main__':
    # 初始化4个消息队列
    url_q = Queue()
    result_q = Queue()
    conn_q = Queue()
    store_q = Queue()
    # 创建分布式管理器
    node = NodeManager()
    freeze_support()
    manager = node.start_manager(url_q, result_q)
    # 创建url管理进程、数据提取进程和数据存储进程
    url_manager_proc = Process(target=node.url_manager_proc, args=(url_q, conn_q, 'https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB'),)
    result_solve_proc = Process(target=node.result_solve_proc, args=(result_q, conn_q, store_q,))
    store_proc = Process(target=node.store_proc, args=(store_q,))
    # 启动进程
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()



