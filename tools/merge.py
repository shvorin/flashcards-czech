#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path
import string
import itertools
from grammar import *
from ftable import *

dirname = os.path.dirname(sys.argv[0])

def checkKey(case, number, gender):
    if type(case) != GrammarCase or type(number) != GrammarNumber or type(gender) != GrammarGender:
        raise KeyError
    if not number in (GrammarNumber.singular, GrammarNumber.plural):
        raise KeyError

# isGreen means that ru-cz isomorphism exists; refer to the spreadsheet
def isGreen_hard_adjective(case, number, gender):
    checkKey(case, number, gender)
    if gender is GrammarGender.feminine and number is GrammarNumber.singular:
        return False
    if case in (GrammarCase.nominative, GrammarCase.accusative, GrammarCase.vocative):
        if number is GrammarNumber.plural or gender is GrammarGender.neuter:
            return False
    return True

def isGreen_soft_adjective(case, number, gender):
    checkKey(case, number, gender)
    # don't bother with it
    return False

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
                             GrammarGender.neuter: 'město',
                         })
    # tags
    tPossessive, tHard, tSoft = 1, 2, 3
    lexemes = {tPossessive: read_forms(Adjective_FTable, 'pronouns', 'svůj', split_variants),
               tHard:       read_forms(Adjective_FTable, 'adjectives', 'mladý', split_variants),
               tSoft:       read_forms(Adjective_FTable, 'adjectives', 'jarní', split_variants)
    }

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
                for tag, lexeme in lexemes.iteritems():
                    if tag is tHard and isGreen_hard_adjective(case, number, gender):
                        continue
                    if tag is tSoft and isGreen_soft_adjective(case, number, gender):
                        continue
                    try:
                        # use only one variant for the lefthand side
                        nominative = lexeme.get(GrammarCase.nominative, number, gender)[0]
                        current = lexeme.get(case, number, gender)
                    except KeyError:
                        continue
                    n_vars = len(current)
                    if tag is tPossessive:
                        # Here we rely on "svůj" database file format: the
                        # _last_ variant is trivial (i.e. the same as in hard
                        # adjetives) and, thus, is to be dropped
                        current = current[:-1]
                        n_vars -= 1
                    if n_vars < 1:
                        continue
                    nominative_pattern.append("[%s (x%d)]" % (nominative, n_vars) if n_vars > 1
                                              else "[%s]" % nominative)
                    current_forms.append(current)

                if not nominative_pattern or not current_forms:
                    continue

                lefthand = "%s %s %s" % (prefix, ' '.join(nominative_pattern), postfix)
                righthand = ' / '.join([' '.join(x) for x in itertools.product(*current_forms)])

                print "%s\t%s" % (lefthand, righthand)
