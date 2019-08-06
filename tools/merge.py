#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path
import string
import itertools
from grammar import *

dirname = os.path.dirname(sys.argv[0])

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
            for number_idx, number in enumerate(Adjective_FTable.number_list):
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

def mk_case_dict(*lst):
    if len(lst) == 1:
        lst = string.split(lst[0], ' ')
    res = {}
    for idx, val in enumerate(lst):
        if not val is None:
            res[GrammarCase(idx + 1)] = val
    return res

def map_dict(f, t):
    res = {}
    for k, v in t.iteritems():
        res[k] = f(v)
    return res

def split_variants(cell):
    # relying on strict format
    variants = string.split(cell, ' / ')
    def clean(s):
        return string.strip(string.rstrip(s))
    return map(clean, variants)

def uniq_variant(cell):
    # presuming that the first variant is the most common
    return split_variants(cell)[0]

# TODO: exploit corrlation between ctor and group
def read_forms(ctor, group, word, convert):
    # TODO: check if the group and word exist in the database
    return ctor(os.path.join(dirname, '../database', group, word),
                convert)

if __name__ == '__main__':
    # NB: avoid mutable prepositions (like s/se, k/ke, v/ve)
    aux_prefix = mk_case_dict("to je/jsou", "bez", "díky", "vidím", "ahoj,", "o", "před")

    aux_nouns = map_dict(lambda word: read_forms(Noun_FTable, 'nouns', word, uniq_variant),
                         {
                             GrammarGender.masculine_animate: 'bratr',
                             GrammarGender.masculine_inanimate: 'strom',
                             GrammarGender.feminine: 'bříza',
                             GrammarGender.neuter: 'slunce',
                         })
    lexemes = (read_forms(Adjective_FTable, 'pronouns', 'svůj', split_variants),
               read_forms(Adjective_FTable, 'adjectives', 'mladý', split_variants),
               read_forms(Adjective_FTable, 'adjectives', 'jarní', split_variants))

    for number in GrammarNumber.__members__.itervalues():
        for gender in GrammarGender.__members__.itervalues():
            for case in GrammarCase.__members__.itervalues():
                if case in (GrammarCase.nominative, GrammarCase.vocative):
                    continue
                
                try:
                    prefix = aux_prefix[case]
                    postfix = aux_nouns[gender].get(case, number)
                except KeyError:
                    continue

                nominative_pattern = []
                current_forms = []
                for lexeme in lexemes:
                    # use only one variant for the lefthand side
                    nominative = lexeme.get(GrammarCase.nominative, number, gender)[0]
                    current = lexeme.get(case, number, gender)
                    n_vars = len(current)
                    nominative_pattern.append("[%s (x%d)]" % (nominative, n_vars) if n_vars > 1
                                              else "[%s]" % nominative)
                    current_forms.append(current)

                lefthand = "%s %s %s" % (prefix, ' '.join(nominative_pattern), postfix)
                righthand = ' / '.join([' '.join(x) for x in itertools.product(*current_forms)])

                print "%s\t%s" % (lefthand, righthand)
