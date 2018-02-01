# coding: utf-8
import re
import urllib.parse
from bs4 import BeautifulSoup


# 本模块用于解析网页
class HtmlParse(object):
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    # 从网页获取url
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # 将百科页面的链接拼接为完整链接并加入元组
        links = soup.find_all('a', href=re.compile(r'/item/.*'))
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls

    # 从网页获取数据
    def _get_new_data(self, page_url, soup):
        data = {}
        data['url'] = page_url
        # 获取标题
        title = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.get_text()
        # 获取概述
        summary = soup.find('div', class_='lemma-summary')
        data['summary'] = summary.get_text()
        return data
