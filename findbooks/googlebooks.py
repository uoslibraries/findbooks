# -*- coding: utf-8 -*-
from findbooks.checker import *


class GoogleChecker(Checker):

    def __inti__(self):
        self.query_url = None

    def _build_query(self, item):
        baseurl = 'https://www.googleapis.com/books/v1/volumes?'
        params = ['q=',
                  urllib.parse.quote_plus(str(item.year)) if item.year else '',
                  '+',
                  'intitle%3A',
                  ('%22' + urllib.parse.quote_plus(str(item.title)) + '%22') if item.title else '',
                  '+',
                  'inauthor%3A',
                  urllib.parse.quote_plus(str(item.author)) if item.author else '',
                  '&',
                  'filter=full']
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
                resp = json.load(io.StringIO(html))
                if resp['totalItems'] == 0:
                    return item, hits
                else:
                    # get record urls for each hit (limit 10)
                    records = dict()
                    docs = resp['items']
                    for result in docs:
                        identifier = result['id']
                        record_url = result['canonicalVolumeLink']
                        records[identifier] = record_url
                    if records:
                        for record in records.keys():
                            hits.append(records[record])
        return item, hits