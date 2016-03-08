# -*- coding: utf-8 -*-
from findbooks.checker import *


class IaChecker(Checker):

    def __inti__(self):
        self.queryurl = None

    def _build_query(self, item):
        baseurl = 'https://archive.org/advancedsearch.php?'
        params = ['q=title%3A%22',
                  urllib.parse.quote_plus(str(item.title)) if item.title else '',
                  '%22+AND+',
                  'creator%3A%22',
                  urllib.parse.quote_plus(str(item.author)) if item.author else '',
                  '%22+AND+',
                  'date%3A%22',
                  urllib.parse.quote_plus(str(item.year)) if item.year else '',
                  '%22&',
                  'fl%5B%5D=identifier&',
                  'sort%5B%5D=&',
                  'sort%5B%5D=&',
                  'sort%5B%5D=&',
                  'rows=10&',
                  'page=1&',
                  'output=json&',
                  'callback=callback&',
                  'save=yes#raw']
        self.queryurl = baseurl + "".join(params)
