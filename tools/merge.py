#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path
import string
import itertools
from grammar import *

dirname = os.path.dirname(sys.argv[0])

# maps (gender, number) to (file, column)
def possessive_pronoun(gender, number):
    def f():
        if gender is GrammarGender.masculine_animate:
            return "svůj-m-živ"
        if gender is GrammarGender.masculine_inanimate:
            return "svůj-m-neživ"
        if gender is GrammarGender.feminine:
            return "svá"
        if gender is GrammarGender.neuter:
            return "své"
    def g():
        if number is GrammarNumber.singular:
            return 2
        if number is GrammarNumber.plural:
            return 3
    return os.path.join(dirname, "..", "pronouns", f()), g()

def adjective(hard, gender, number):
    def f():
        if gender is GrammarGender.masculine_animate:
            return "m-živ"
        if gender is GrammarGender.masculine_inanimate:
            return "m-neživ"
        if gender is GrammarGender.feminine:
            return "ž"
        if gender is GrammarGender.neuter:
            return "s"
    def g():
        if number is GrammarNumber.singular:
            return "jed"
        if number is GrammarNumber.plural:
            return "mn"
    def h():
        if gender is GrammarGender.masculine_animate:
            return 1
        if gender is GrammarGender.masculine_inanimate:
            return 2
        if gender is GrammarGender.feminine:
            return 3
        if gender is GrammarGender.neuter:
            return 4

    part1 = f()
    part2 = g()
    if part1 is None or part2 is None:
        return (None, None)
    if hard:
        adj = "mladý"
    else:
        adj = "jarní"
    if number is GrammarNumber.plural:
        # ignore gender
        fname = '-'.join([adj, part2])
    else:
        fname = '-'.join([adj, part2, part1])

    fname = os.path.join(dirname, "..", "adj", fname)
    if not hard or number is GrammarNumber.singular:
        column = 1
    else:
        column = h()
    return fname, column

case_questions = [
    "kdo, co",
    "koho, čeho",
    "komu, čemu",
    "koho, co",
    "o kom, o čem",
    "s kým, čím"]

# NB: avoid mutable prepositions (like s/se, k/ke, v/ve)
case_prefix = {
    GrammarCase.nominative: "to je/jsou",
    GrammarCase.genitive: "bez",
    GrammarCase.dative: "díky",
    GrammarCase.accusative: "vidím",
    # skip GrammarCase.vocative
    GrammarCase.locative: "o",
    GrammarCase.instrumental: "před"
    }

for gender in GrammarGender.__members__.itervalues():
    for number in GrammarNumber.__members__.itervalues():
        fname_columns = (possessive_pronoun(gender, number),
                         adjective(True, gender, number),
                         adjective(False, gender, number))
        try:
            files_columns = [(open(fname), col) for fname, col in fname_columns]

            for i in GrammarCase.__members__.itervalues():
                if i is GrammarCase.vocative:
                    continue
                s = []
                multivar = False
                for f, col in files_columns:
                    line = f.readline()
                    if not line:
                        break
                    line = line[:-1] # drop '/n'
                    form = string.split(line, '\t')[col - 1]
                    form_vars = string.split(form, ', ')
                    s.append(form_vars)
                    if len(form_vars) > 1:
                        multivar = True

                if not s:
                    break

                if i is GrammarCase.nominative:
                    # take only one variant for the lefthand side
                    nominative = ' '.join(["[" + el[0] + "]" for el in s])
                else:
                    # try:
                    #     qcase = case_questions[i]
                    # except IndexError:
                    #     break
                    try:
                        pre = case_prefix.get(i, "")
                    except Exception, e:
                        print e
                    lefthand = "%s %s" % (pre, nominative)
                    if multivar:
                        lefthand += " (několik variant)"
                    # generate all variants for the righthand side
                    righthand = ', '.join([' '.join(x) for x in itertools.product(*s)])
                    print "%s\t%s" % (lefthand, righthand)

            for f, _ in files_columns:
                f.close()
        except:
            continue
