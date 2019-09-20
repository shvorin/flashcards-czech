#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from grammar import *

class Raw_FTable(object):
    def __init__(self, fname, convert=None):
        if convert is None:
            convert = lambda x: x
        t = {}
        nCols_min = 0
        nCols_max = 0
        row = 0
        with open(fname) as f:
            lines = f.readlines()
            self.nRows = len(lines)
            for line in lines:
                line = line.rstrip() # remove trailing '\n'
                col = 0
                items = string.split(line, '\t')
                for item in items:
                    t[(row, col)] = convert(item)
                    col += 1
                row += 1
                nItems = len(items)
                if nCols_min == 0 or nItems < nCols_min:
                    nCols_min = nItems
                if nItems > nCols_max:
                    nCols_max = nItems
        self.raw_table = t
        self.nCols = nCols_max
        self.straight = nCols_min == nCols_max

class Noun_FTable(Raw_FTable):
    """
singulár | plurál
"""
    number_list = GrammarNumber.singular, GrammarNumber.plural

    def __init__(self, fname, convert=None):
        super(Noun_FTable, self).__init__(fname, convert)
        t = {}
        for case in GrammarCase.__members__.itervalues():
            for number_idx, number in enumerate(Noun_FTable.number_list):
                # NB: column zero stands for case names, so must be skipped
                col = number_idx + 1
                row = case.value - 1
                try:
                    t[(case, number)] = self.raw_table[(row, col)]
                except KeyError:
                    pass
        self.noun_table = t

    def get(self, case, number):
        return self.noun_table[(case, number)]

class Adjective_FTable(Raw_FTable):
    """
Číslo |	           singulár           |             plurál
Rod   | m. živ. | m. neživ. | ž. | s. | m. živ. | m. neživ. | ž. | s.

This format is also suitable for possessive pronouns.
"""
    number_list = GrammarNumber.singular, GrammarNumber.plural

    def __init__(self, fname, convert=None):
        super(Adjective_FTable, self).__init__(fname, convert)
        t = {}
        for case in GrammarCase.__members__.itervalues():
            for number_idx, number in enumerate(self.number_list):
                for gender_idx, gender in enumerate(GrammarGender.__members__.values()):
                    # NB: column zero stands for case names, so must be skipped
                    col = number_idx * len(GrammarGender) + gender_idx + 1
                    row = case.value - 1
                    try:
                        t[(case, number, gender)] = self.raw_table[(row, col)]
                    except KeyError:
                        pass
        self.adjective_table = t

    def get(self, case, number, gender):
        return self.adjective_table[(case, number, gender)]
