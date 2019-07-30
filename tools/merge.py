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
    part1 = f()
    part2 = g()
    if part1 is None or part2 is None:
        return (None, None)
    if hard:
        adj = "mladý"
    else:
        adj = "jarní"
    if not hard and number is GrammarNumber.plural:
        # ignore gender
        fname = '-'.join([adj, part2])
    else:
        fname = '-'.join([adj, part2, part1])

    fname = os.path.join(dirname, "..", "adj", fname)
    column = 1
    return fname, column

case_questions = [
    "kdo, co",
    "koho, čeho",
    "komu, čemu",
    "koho, co",
    "o kom, o čem",
    "s kým, čím"]

for gender in GrammarGender.__members__.itervalues():
    for number in GrammarNumber.__members__.itervalues():
        fname_columns = (possessive_pronoun(gender, number),
                         adjective(True, gender, number),
                         adjective(False, gender, number))
        try:
            files_columns = [(open(fname), col) for fname, col in fname_columns]

            i = 0
            while True:
                s = []
                for f, col in files_columns:
                    line = f.readline()
                    if not line:
                        break
                    line = line[:-1] # drop '/n'
                    var = string.split(line, '\t')[col - 1]
                    xxx = string.split(var, ', ')
                    s.append(xxx)
                if not s:
                    break

                if i == 0:
                    nominative = ' '.join([', '.join(el) for el in s])
                else:
                    try:
                        qcase = case_questions[i]
                    except IndexError:
                        break
                    expr = ', '.join([' '.join(x) for x in itertools.product(*s)])
                    print "%s |%s>\t%s" % (nominative, qcase, expr)
                i += 1

            for f, _ in files_columns:
                f.close()
        except:
            continue
