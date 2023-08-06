#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from refinery.units.meta import Arg, ConditionalUnit


class iffs(ConditionalUnit):
    """
    Filter incoming chunks depending on whether they contain a given binary substring.
    """
    def __init__(self, needle: Arg(help='the string to search for'), negate=False, temporary=False):
        super().__init__(negate=negate, temporary=temporary, needle=needle)

    def match(self, chunk):
        return self.args.needle in chunk
