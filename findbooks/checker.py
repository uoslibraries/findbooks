# -*- coding: utf-8 -*-
import io
import json
import re
import urllib


class Checker:
    """
    Base class for creating checker objects,
    which check a specified catalogue for
    title, author and date matches
    """

    def _build_query(self, item):
        pass

    def check(self, item):
        pass
