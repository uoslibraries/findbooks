# -*- coding: utf-8 -*-
from findbooks.checker import *


class IaChecker(Checker):

    def __init__(self):
        self.query_url = None

    def _build_query(self, item):
        baseurl = 'https://archive.org/advancedsearch.php?'
        params = ['q=title%3A',
                  ('%22' + urllib.parse.quote_plus(str(item.title)) + '%22') if item.title else '',
                  '+AND+',
                  'creator%3A',
                  ('%22' + urllib.parse.quote_plus(str(item.author)) + '%22') if item.author else '',
                  '+AND+',
                  'date%3A',
                  ('%22' + urllib.parse.quote_plus(str(item.year)) + '%22') if item.year else '',
                  '&',
                  'fl%5B%5D=identifier&',
                  'sort%5B%5D=&',
                  'sort%5B%5D=&',
                  'sort%5B%5D=&',
                  'rows=10&',
                  'page=1&',
                  'output=json&',
                  'callback=callback&',
                  'save=yes#raw']
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
                html = html[9:-1]
                resp = json.load(io.StringIO(html))
                if resp['response']['numFound'] == 0:
                    return item, hits
                else:
                    # get record urls for each hit (limit 10)
                    records = dict()
                    docs = resp['response']['docs']
                    for result in docs:
                        identifier = result['identifier']
                        record_url = 'https://archive.org/details/' + identifier
                        records[identifier] = record_url
                    if records:
                        for record in records.keys():
                            hits.append(records[record])
        return item, hits
