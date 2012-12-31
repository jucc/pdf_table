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
