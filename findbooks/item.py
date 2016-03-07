# -*- coding: utf-8 -*-
import io
import urllib.request
from pymarc import MARCReader


class Item:
    """
    Represents an item from our
    Library catalogue (https://www-lib.soton.ac.uk)
    Usage:

        #>>> import findbooks
        #>>> item = findbooks.Item('12345678')
        #>>> item.getMarcFields()
        #>>> print(item.title)

    """
    webcat = "http://lms.soton.ac.uk/cgi-bin/goobi_marc.cgi?itemid="

    def __init__(self, barcode):
        self.barcode = barcode
        self.marc = None
        self.record = None
        self.title = None
        self.author = None
        self.year = None

    def _get_marc(self):
        with urllib.request.urlopen(Item.webcat + self.barcode) as response:
            html = response.read().decode("utf-8")
            marc = html[html.find(">")+1:html.rfind("<")].strip('''

 ''')
            if "Barcode not found" not in marc:
                self.marc = marc

    def _get_title(self):
        # strip trailing '/' from subfield 'a' only results
        title = self.record.title().strip(" /")
        return title

    def _get_author(self):
        if self.record['100']:
            return self.record['100']['a']
        elif self.record['110']:
            return self.record['110']['a']
        elif self.record['111']:
            return self.record['111']['a']
        else:
            return None

    def _get_year(self):
        date = self.record.pubyear()
        if date:
            # dates should only have numbers
            nums = '1234567890'
            new_date = ''
            for ch in date:
                if ch in nums:
                    new_date += ch
            # dates should have '1' as the first char
            if not new_date[0] == 1:
                return None
            # dates should eb 4 chars long
            if not len(date) == 4:
                return None
            return new_date
        else:
            return None

    def get_marc_fields(self):
        self._get_marc()
        if self.marc:
            with io.BytesIO(self.marc.encode('utf-8')) as fh:
                reader = MARCReader(fh)
                for record in reader:
                    self.record = record
                    self.title = self._get_title()
                    self.author = self._get_author()
                    self.year = self._get_year()

# item = Item('59571478')
# item.get_marc_fields()
# print(item.title)
