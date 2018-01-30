# coding: utf-8
import re
import urllib.parse
from bs4 import BeautifulSoup


# 本模块用于解析网页
class HtmlParse(object):
    def parse(self, page_url, html_cont):
