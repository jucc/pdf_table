#!/usr/bin/env/python
# -*- coding: utf-8 -*-

def get_grade(line, weights):
    pass

def get_chem_eng(lines):
    is_chemeng = lambda x: x[7] != None and x[8] != None
    return filter(is_chemeng, lines)
