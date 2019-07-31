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

# case_questions = [
#     "kdo, co",
#     "koho, čeho",
#     "komu, čemu",
#     "koho, co",
#     "o kom, o čem",
#     "s kým, čím"]

def mk_case_dict(*lst):
    if len(lst) == 1:
        lst = string.split(lst[0], ' ')
    res = {}
    for idx in range(len(lst)):
        x = lst[idx]
        if not x is None:
            res[GrammarCase(idx + 1)] = x
    return res

# NB: avoid mutable prepositions (like s/se, k/ke, v/ve)
case_prefix = mk_case_dict("to je/jsou", "bez", "díky", "vidím", "ahoj,", "o", "před")

noun1_jed = mk_case_dict("bratr bratra bratru bratra bratře bratru bratrem")
noun1_mn = mk_case_dict("bratři bratrů bratrům bratry bratři bratrech bratřími")
noun2_jed = mk_case_dict("strom stromu stromu strom strome stromě stromem")
noun2_mn = mk_case_dict("stromy stromů stromům stromy stromy stromech stromy")
noun3_jed = mk_case_dict("bříza břízy bříze břízu břízo bříze břízou")
noun3_mn = mk_case_dict("břízy bříz břízám břízy břízy břízách břízami")
noun4_jed = mk_case_dict("slunce slunce slunci slunce slunce slunci sluncem")
noun4_mn = mk_case_dict("slunce sluncí sluncím slunce slunce sluncích slunci")

case_postfix = {
    (GrammarGender.masculine_animate, GrammarNumber.singular): noun1_jed,
    (GrammarGender.masculine_animate, GrammarNumber.plural): noun1_mn,
    (GrammarGender.masculine_inanimate, GrammarNumber.singular): noun2_jed,
    (GrammarGender.masculine_inanimate, GrammarNumber.plural): noun2_mn,
    (GrammarGender.feminine, GrammarNumber.singular): noun3_jed,
    (GrammarGender.feminine, GrammarNumber.plural): noun3_mn,
    (GrammarGender.neuter, GrammarNumber.singular): noun4_jed,
    (GrammarGender.neuter, GrammarNumber.plural): noun4_mn,
}

for gender in GrammarGender.__members__.itervalues():
    for number in GrammarNumber.__members__.itervalues():
        fname_columns = (possessive_pronoun(gender, number),
                         adjective(True, gender, number),
                         adjective(False, gender, number))
        try:
            files_columns = [(open(fname), col) for fname, col in fname_columns]
            forms = {}

            for i in GrammarCase.__members__.itervalues():
                if i is GrammarCase.vocative:
                    # the database files have vocative skipped
                    continue
                forms[i] = []
                for f, col in files_columns:
                    line = f.readline()
                    if not line:
                        break
                    line = line[:-1] # drop '/n'
                    form = string.split(line, '\t')[col - 1]
                    form_vars = string.split(form, ', ')
                    forms[i].append(form_vars)

            # TODO: use a random form for the pattern
            s_pat = forms[GrammarCase.nominative]
            for i, s in forms.iteritems():
                if i is GrammarCase.nominative:
                    continue

                # use only one variant for the lefthand side
                nominative_pattern = []
                assert len(s_pat) == len(s)
                for idx in range(len(s_pat)):
                    l = len(s[idx])
                    elem = "[%s (x%d)]" % (s_pat[idx][0], l) if l > 1 else "[%s]" % s_pat[idx][0]
                    nominative_pattern.append(elem)

                try:
                    prefix = case_prefix[i]
                    postfix = case_postfix[(gender, number)][i]
                except KeyError:
                    continue

                lefthand = "%s %s %s" % (prefix, ' '.join(nominative_pattern), postfix)

                # generate all variants for the righthand side
                righthand = ' / '.join([' '.join(x) for x in itertools.product(*s)])
                print "%s\t%s" % (lefthand, righthand)

            for f, _ in files_columns:
                f.close()
        except:
            continue