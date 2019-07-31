#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum, unique

GrammarNumber = Enum('GrammarNumber', 'singular plural dual')

GrammarGender = Enum('GrammarGender', 'masculine_animate masculine_inanimate feminine neuter')

GrammarAnimacy = Enum('GrammarAnimacy', 'animate inanimate')

# TODO: GrammarCase
