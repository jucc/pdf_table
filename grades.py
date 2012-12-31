#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from conf import *

def get_chem_eng(lines):
    is_chemeng = lambda x: x[fis] != None and x[mat] != None
    return filter(is_chemeng, lines)


def get_grade(line):
    return 2*float(line[mat]) + float(line[fis]) + float(line[red])


def grade_students(lines):
    for line in lines:
        line.append(get_grade(line))


def sort_grades(lines):
    sort_by_final_grade = lambda x: (x[-1], x[mat], x[fis], x[red])
    lines.sort(key=sort_by_final_grade, reverse=True)


def rank(lines):
    grade_students(lines)
    sort_grades(lines)
