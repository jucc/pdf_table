#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pdf import get_doc_pages, get_page_elements, extract_text_elements

avg_height = 12
avg_width = 27
deviation = 0.5

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
        blocks = [Block(tb.x0, tb.y0, tb.get_text()) for tb in text_elements] 
        return blocks

    @staticmethod
    def strip_metadata(blocks):
        is_data = lambda b: not(b.contains('/') or b.contains(':') or b.contains('Exame Discursivo') or b.contains('Nome do Candidato'))
        return filter(is_data, blocks)
    

def update_average(old_avg, old_len, new_value):
    return (old_avg * old_len + new_value) / (old_len + 1)

def find_partitions(text):
    lines = []
    cols = []
    for block in text:

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
        lines.sort()

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
    
def fixed_table(lines, cols):
    table = []
    for i in range (len(lines)):
        line = []
        for j in range (len(cols)):
            line.append(None)
        table.append(line)
    return table

def assemble_table(blocks):
    lines, cols = find_partitions(blocks)
    table = fixed_table(lines, cols)

    for block in blocks:
        pass

if __name__ == "__main__":
    pages = get_doc_pages('/home/ju/Downloads/A_B.pdf')
    page = pages.next()    
    text = extract_text_elements(page)
    blocks = Block.strip_metadata(Block.convert_to_blocks(text))
    print_blocks(blocks)
    print fixed_table(range(3), range(4))

