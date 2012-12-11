#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reads a pdf document and converts it into a table
Reference for pdfminer work: http://denis.papathanasiou.org/?tag=pdfminer
"""

from pdfminer.pdfparser import PDFParser, PDFDocument, PDFNoOutlines
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage

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
    text_blocks = filter(istext, page_elements)
    return [line for block in text_blocks for line in block]

def belongs_to_partition(value, avg, partition_size):
    return abs(value - avg) < partition_size * 0.5

def update_average(old_avg, old_len,  new_value):
    return (old_avg * old_len + new_value) / (old_len + 1)

def find_blocks(text, avg_line_height, avg_col_width):
    lines = []
    cols = []
    for block in text:

        for x_col in cols:
            if belongs_to_partition(block.x0, x_col, avg_col_width):
                x_col = update_average(x_col, len(cols) - 1, block.x0)
                break
        else:
            cols.append(block.x0)
        cols.sort()

        for y_line in lines:
            if belongs_to_partition(block.y0, y_line, avg_line_height):
                y_line = update_average(y_line, len(lines) - 1, block.y0)
                break
        else:
            lines.append(block.y0)
        lines.sort()

    return lines, cols

def strip_metadata(text):
    """
    Works only for UERJ grade template specific pdf
    """
    contains = lambda bl, tx: bl.get_text().find(tx) != -1
    not_meta = lambda b: not (contains(b, '/') or contains(b, ':') or contains(b, 'Exame Discursivo') or contains(b, 'Nome do Candidato'))
    return filter(not_meta, text)

def create_table(blocks, lines, cols):    
 
    for line_number in lines:
        print "[%.01f]" % line_number
    #       for cell in lines[line_number]:
    #           print cell.get_text().encode('utf-8')
    for col in cols:
        print "[%.01f]" % col
    return len(lines), len(cols)

if __name__ == "__main__":
    pages = get_doc_pages('/home/ju/Downloads/A_B.pdf')
    page = pages.next() # for i, page in enumerate(pages):
    text = strip_metadata(get_text_elements(page))
    create_table(text, *find_blocks(text, 11.5, 26.5))
