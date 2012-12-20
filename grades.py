#!/usr/bin/env/python
# -*- coding: utf-8 -*-


def get_chem_eng(lines):
    is_chemeng = lambda x: x[7] != None and x[8] != None
    return filter(is_chemeng, lines)


def get_grade(line):
    return float(line[8]) * 2 + float(line[7]) + float(line[9]) + 20


def grade_students(lines):
    for line in lines:
        line.append(get_grade(line))


def sort_grades(lines):
    sort_by_final_grade = lambda x: (x[-1], x[-3], x[-4], x[-2])
    lines.sort(key=sort_by_final_grade, reverse=True)


def rank(lines):
    grade_students(lines)
    sort_grades(lines)
