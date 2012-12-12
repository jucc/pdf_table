#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reads a pdf document and converts it into a table
Reference for pdfminer work: http://denis.papathanasiou.org/?tag=pdfminer
"""

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

avg_height = 12
avg_width = 27
deviation = 0.5

def get_doc_pages(filename):
    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize()
    return doc.get_pages()

def get_page_elements(page):
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    interpreter.process_page(page)
    return device.get_result()

def get_text_elements(page):
    page_elements = get_page_elements(page)
    istext = lambda el: isinstance(el, LTTextBox) or isinstance(el, LTTextLine)
    return filter(istext, page_elements)


class Block:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def contains(self, tx):
        return self.text.find(tx) != -1

    def belongs_to_column(self, x_col):
        return Block.belongs_to_partition(self.x, x_col, avg_width)

    def belongs_to_line(self, y_line):
        return Block.belongs_to_partition(self.y, y_line, avg_height)
    
    @staticmethod
    def belongs_to_partition(value, avg, partition_size):
        return abs(value - avg) < partition_size * deviation
        
    @staticmethod
    def convert_to_blocks(text_elements):
    """
    Extracts pdfminer's LTTextLines and LTTextBox elements into simple text blocks (only x0, y0 and text)
    """
    blocks = [Block(tb.x0, tb.y0, tb.get_text()) for boxes in text_elements for tb in boxes])

    @staticmethod
    def strip_metadata(blocks):
    """
    Removes metadata blocks (title, report header, footer, table header)
    Works only for UERJ grade template specific pdf.
    """    
        data = lambda b: not(b.contains('/') or b.contains(':') or b.contains('Exame Discursivo') or b.contains('Nome do Candidato'))
        return filter(data, blocks)
    
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

def sort_table(text): 
    lines, cols = find_partitions(text)
    for line_number in lines:
        print "[%.01f]" % line_number
    #       for cell in lines[line_number]:
    #           print cell.get_text().encode('utf-8')
    for col in cols:
        print "[%.01f]" % col
    return len(lines), len(cols)
    
def extract_table(page):
    elements = get_text_elements(page)    
    text = Block.strip_metadata(Block.convert_to_blocks(text))
    sort_table(text)

if __name__ == "__main__":
    pages = get_doc_pages('/home/ju/Downloads/A_B.pdf')
    page = pages.next() # for i, page in enumerate(pages):
    table = extract_table(page)
    
