#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def target_case(i):
    if i <= 3:
        return "%d. pád" % (i+1)
    if i <= 5:
        return "%d. pád" % (i+2)
    return ""

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

    xx = ' '.join(s)
    if i == 0:
        nominative = xx
    else:
        print "%s |%s>\t%s" % (nominative, target_case(i), xx)
    i += 1

for f in files:
    f.close()
