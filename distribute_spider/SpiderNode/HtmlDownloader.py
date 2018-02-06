# coding: utf-8
import requests


# 本模块用于下载网页
class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/63.0.3239.132 ' \
                     'Safari/537.36'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None