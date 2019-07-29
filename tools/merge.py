#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

case_questions = [
    "kdo, co",
    "koho, čeho",
    "komu, čemu",
    "koho, co",
    "o kom, o čem",
    "s kým, čím"]

files = map(open, sys.argv[1:])

i = 0
while True:
    s = []
    for f in files:
        line = f.readline()
        if not line:
            break
        line = line[:-1] # drop '/n'
        s.append(line)
    if not s:
        break

    expr = ' '.join(s)
    if i == 0:
        nominative = expr
    else:
        try:
            qcase = case_questions[i]
        except IndexError:
            break
        print "%s |%s>\t%s" % (nominative, qcase, expr)
    i += 1

for f in files:
    f.close()
