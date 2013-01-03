#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conf import *
from block import *
   

def update_average(old_avg, old_len, new_value):
    return (old_avg * old_len + new_value) / (old_len + 1)


def find_lines(blocks):
    lines = []
    while len(blocks) > 0:
        cur_line = [b for b in blocks if b.belongs_to_line(blocks[0].y)]
        dic = {'height':cur_line[0].y, 'blocks':cur_line}
        lines.append(dic)
        blocks = [b for b in blocks if b not in cur_line]
        
    sort_lines = lambda x: x['height']
    lines.sort(key=sort_lines, reverse=True)
    #removes header
    return lines[1:]


def find_cols(blocks):
    if use_fix_columns: #cols defined in conf.py
        cols = fix_columns
    else:
        cols = []
        for block in blocks:
            for x_col in cols:
                if block.belongs_to_column(x_col):
                    x_col = update_average(x_col, len(cols)-1, block.x)
                    break
            else:
                cols.append(block.x)
        cols.sort()
    return cols
   

def assemble_table(blocks):
    cols = find_cols(blocks)
    lines = find_lines(blocks)
    for line in lines:
        line['cols'] = [None]*len(cols)
        for block in line['blocks']:
            insert_cols(block, line['cols'], cols)
    return map(lambda x: x['cols'], lines)


def insert_cols(block, line, cols):
    """Addresses a problem where two adjacent cells are so
    close that the pdf recognizes only one block"""
    col = block.find_col(cols)
    if col == 0:
        line[0] = get_name(block.text)
    else:
        cells = block.text.split(' ')
        for i in range(0, len(cells)):
            line[col + i] = replace(cells[i])


def get_name(col):
    return ' '.join(col.split(' ')[1:])


def replace(text):
    text = text.replace(',', '.')    
    if text == 'FALTA' or text == 'ELIM':
        text = '0.0'
    return text
