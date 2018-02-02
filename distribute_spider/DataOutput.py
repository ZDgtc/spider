# coding:utf-8
import codecs
import time


class DataOutput(object):

    # 实例化之后创建html文件，写入头部，并初始化data集合
    def __init__(self):
        self.filepath = 'baike_%s.html' % time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
        self.output_head(self.filepath)
        self.data = []

    def store_data(self, data):
        if data is None:
            return
        self.data.append(data)
        # 内存缓存10个data数据，然后写入文件
        if len(self.data) > 10:
            self.output_html(self.filepath)

    def output_head(self, filepath):
        fout = codecs.open(filepath, 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        fout.close()

    def output_html(self, filepath):
        fout = codecs.open(filepath, 'a', encoding='utf-8')
        for data in self.data:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % data['url'])
            fout.write('<td>%s</td>' % data['title'])
            fout.write('<td>%s</td>' % data['summary'])
            fout.write('</tr>')
            self.data.remove(data)
        fout.close()

    def output_end(self, filepath):
        fout = codecs.open(filepath, 'w', encoding='utf-8')
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()