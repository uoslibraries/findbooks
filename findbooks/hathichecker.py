# -*- coding: utf-8 -*-
from findbooks.checker import *


class HathiChecker(Checker):

    def __init__(self):
        self.query_url = None

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
        self.query_url = baseurl + "&".join(params)

    def check(self, item):
        """
        Method takes an item and returns a tuple
        containing the item and a list of hits.
        """
        hits = []
        # item must have a title to proceed
        if item.title:
            self._build_query(item)
            with urllib.request.urlopen(self.query_url) as response:
                html = response.read().decode('utf-8')
                if 'class="error"' in html:
                    # 'class="error"' indicates no hits
                    return item, hits
                else:
                    # get record urls for each hit on page 1
                    matches = [m.start() for m in re.finditer('<a href="/Record/', html)]
                    records = dict()
                    for match in matches:
                        start = match + 9
                        end = match +26
                        record_url = 'http://catalog.hathitrust.org' + html[start:end]
                        hathi_ident = html[start+8:end]
                        records[hathi_ident] = record_url
                    if records:
                        for record in records.keys():
                            with urllib.request.urlopen(records[record]) as response:
                                html = response.read().decode('utf-8')
                                if 'class="rights-pd fulltext"' in html:
                                    hits.append(records[record])
        return item, hits
