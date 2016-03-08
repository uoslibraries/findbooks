# -*- coding: utf-8 -*-
from findbooks.checker import *


class HathiChecker(Checker):

    def __inti__(self):
        self.queryurl = None

    def _build_query(self, item):
        baseurl = 'http://catalog.hathitrust.org/Search/Home?'
        params = ['adv=1',
                  'type%5B%5D=title',
                  'lookfor%5B%5D=' + urllib.parse.quote(str(item.title)) if item.title else '',
                  'bool%5B%5D=AND',
                  'type%5B%5D=author',
                  'lookfor%5B%5D=' + urllib.parse.quote(str(item.author)) if item.author else '',
                  'bool%5B%5D=AND',
                  'type%5B%5D=year',
                  'lookfor%5B%5D=' + urllib.parse.quote(str(item.year)) if item.year else '',
                  'bool%5B%5D=AND',
                  'type%5B%5D=subject',
                  'lookfor%5B%5D=',
                  'setft=true',
                  'ft=ft',
                  'yop=after',
                  'fqrange-start-publishDateTrie-1=',
                  'fqrange-end-publishDateTrie-1=',
                  'fqor-publishDateTrie%5B%5D=',
                  'submit=Search']
        self.queryurl = baseurl + "&".join(params)


