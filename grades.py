#!/usr/bin/env/python
# -*- coding: utf-8 -*-

def get_grade(line):
    return line[8] * 2 + line[7] + line[9] + 20

def grade_students(lines):
    for line in lines:
        line.append(get_grade(line))

def get_chem_eng(lines):
    is_chemeng = lambda x: x[7] != None and x[8] != None
    return filter(is_chemeng, lines)
