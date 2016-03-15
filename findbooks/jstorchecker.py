# -*- coding: utf-8 -*-
from findbooks.checker import *


class JstorChecker(Checker):

    def __init__(self):
        self.query_url = None

    def _build_query(self, item):
        baseurl = 'http://dfr.jstor.org/?'
        if item.year:
            year = 'year%3A%5B' + str(item.year) + '+TO+' + str(int(item.year) + 1) + '%5D%5E1.0%7C'
        else:
            year = ''
        title = 'ta%3A%22' + urllib.parse.quote_plus(str(item.title)) + '%22%5E1.0&'
        if item.author:
            author = 'cc=daa%3A' + urllib.parse.quote_plus(str(item.author)) + '%5E1.0'
        else:
            author = ''
        params = ['cs=',
                  year,
                  title,
                  'fs=asm1%3Artm1%3Ayrm1&',
                  'view=text&',
                  author]
        self.query_url = baseurl + "".join(params)

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

jstor = JstorChecker()