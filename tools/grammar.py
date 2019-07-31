#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum, unique

GrammarNumber = Enum('GrammarNumber', 'singular plural dual')

GrammarGender = Enum('GrammarGender', 'masculine_animate masculine_inanimate feminine neuter')

GrammarAnimacy = Enum('GrammarAnimacy', 'animate inanimate')

# NB: the order matters, we rely on default enumeration: 1, 2, ... 7
GrammarCase = Enum('GrammarCase',
                   'nominative genitive dative accusative vocative locative instrumental')
