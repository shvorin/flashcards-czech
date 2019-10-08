#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path
import string
import random
from grammar import *
from ftable import *

# FIXME: reuse this code

dirname = os.path.dirname(sys.argv[0])

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

def mk_aux_prefix():
    res = {}
    for number in GrammarNumber.__members__.itervalues():
        for idx, val in enumerate(["bez", "díky", "vidím", "ahoj,", "o", "před"]):
            if not val is None:
                case = GrammarCase(idx + 2)
                res[(case, number)] = val
    res[(GrammarCase.nominative, GrammarNumber.singular)] = "to je"
    res[(GrammarCase.nominative, GrammarNumber.plural)] = "to jsou"
    return res

if __name__ == '__main__':
    # NB: avoid mutable prepositions (like s/se, k/ke, v/ve)
    aux_prefix = mk_aux_prefix()
    aux_possessive = read_forms(Adjective_FTable, 'adjectives', 'mladý', uniq_variant)
    noun = read_forms(Noun_FTable, 'nouns', 'pán', split_variants)
    gender = GrammarGender.masculine_animate

    for number in GrammarNumber.__members__.itervalues():
        for case in GrammarCase.__members__.itervalues():
            if case is GrammarCase.nominative:
                continue
            try:
                current = noun.get(case, number)
                n_vars = len(current)
                righthand = ' / '.join(current)
                prefix = aux_prefix[(case, number)]
                possessive = aux_possessive.get(case, number, gender)
                pattern_form = noun.get(GrammarCase.nominative, number)[0]
                pattern = "[%s (x%d)]" % (pattern_form, n_vars) if n_vars > 1 else "[%s]" % pattern_form
                print '%s %s %s\t%s' % (prefix, possessive, pattern, righthand)
            except KeyError:
                continue
