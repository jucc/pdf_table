#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conf import *

class Block:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def contains(self, tx):
        return self.text.find(tx) != -1

    @staticmethod
    def belongs_to_partition(value, avg, partition_size):
        return abs(value - avg) < partition_size * deviation
        
    def belongs_to_column(self, x_col):
        return Block.belongs_to_partition(self.x, x_col, avg_width)

    def belongs_to_line(self, y_line):
        return Block.belongs_to_partition(self.y, y_line, avg_height)

    def find_line(self, lines):
        for i,l in enumerate(lines):
            if self.belongs_to_line(l):
                return i

    def find_col(self, cols):
        for i,c in enumerate(cols):
            if self.belongs_to_column(c):
                return i

    def find_position(self, lines, cols):
        return (self.find_line(lines), self.find_col(cols))

    @staticmethod
    def convert_to_blocks(text_elements):
        blocks = [Block(tb.x0, tb.y0, tb.get_text().encode('utf-8').strip()) for tb in text_elements] 
        return blocks

    @staticmethod
    def strip_metadata(blocks):
        is_data = lambda b: not(b.contains('/') or b.contains(':') or b.contains('Exame Discursivo') or b.contains('Nome') or (b.contains('UERJ') and b.contains('UEZO')) or b.contains('Faltoso') or b.contains('Vestibular Estadual') or b.contains('Resultado Geral') or b.contains('Inscri')or b.contains('Acertos') or b.contains('Conceito'))
        return filter(is_data, blocks)
    

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
            table[line][0] = block.text
        else:
            cells = block.text.split(' ')
            for i in range(0, len(cells)):
                table[line][col + i] = replace(cells[i])
    return table[1:]
