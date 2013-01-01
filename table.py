#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conf import *
from block import *
   

def update_average(old_avg, old_len, new_value):
    return (old_avg * old_len + new_value) / (old_len + 1)


def find_partitions(text):
    lines = []
    cols = []
    for block in text:
        if use_fix_columns: #cols defined in conf.py
            cols = fix_columns
        else:
            for x_col in cols:
                if block.belongs_to_column(x_col):
                    x_col = update_average(x_col, len(cols) - 1, block.x)
                    break
            else:
                cols.append(block.x)
            cols.sort()
        
        for y_line in lines:
            if block.belongs_to_line(y_line):
                y_line = update_average(y_line, len(lines) - 1, block.y)
                break
        else:
            lines.append(block.y)
        lines.sort(reverse=True)
    return lines, cols



def find_lines(blocks):
    lines = []
    for block in blocks:
        for line in lines:
            if block.belongs_to_line(line['height']):  
                line['height'] = update_average(line['height'], len(line['blocks']), block.y)

                line['blocks'].append(block)
                break
        #block was not on any known line
        else:
            line = {'height': block.y, 'blocks':[block]}
            lines.append(line)

    sort_by_height = lambda l: l['height']
    lines.sort(key=sort_by_height, reverse=True)
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
                    x_col = update_average(x_col, len(cols) - 1, block.x)
                    break
            else:
                cols.append(block.x)
        cols.sort()
        return cols
   

def assemble_table2(blocks):    
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
    print line
    col = block.find_col(cols)
    if col == 0:
        line[0] = block.text.split(' ')[0] + get_name(block.text)
    else:
        cells = block.text.split(' ')
        for i in range(0, len(cells)):
            line[col + i] = replace(cells[i])


def get_name(col):
    return ' '.join(col.split(' ')[1:])

def print_blocks(text): 
    lines, cols = find_partitions(text)
    print 'LINHAS'
    for i, y in enumerate(lines):
        print "[%i] %.01f" % (i, y)
    #       for cell in lines[line_number]:
    #           print cell.get_text().encode('utf-8')
    print 'COLUNAS'
    for j, x in enumerate(cols):
        print "[%i] %.01f" % (j, x)
    return len(lines), len(cols)


def empty_table(lines, cols):
    if isinstance(lines, list): lines = len(lines)
    if isinstance(cols, list): cols = len(cols)
    return [[None]*cols for x in xrange(lines)]

def replace(text):
    text = text.replace(',', '.')    
    if text == 'FALTA' or text == 'ELIM':
        text = '0.0'
    return text

def assemble_table(blocks):
    """
    solves a specific problem in which columns too close together are joined
    must not be used when table may contain spaces in columns other than the first one
    """
    lines, cols = find_partitions(blocks)
    table = empty_table(lines, cols)
    not_header = lambda x: x.find_line(lines) != 0

    for block in filter(not_header, blocks):
        line, col = block.find_position(lines, cols)
        if col == 0 :
            table[line][0] = block.text.split(' ')[0] + get_name(block.text)
        else:
            cells = block.text.split(' ')
            for i in range(0, len(cells)):
                table[line][col + i] = replace(cells[i])
    return table[1:]
