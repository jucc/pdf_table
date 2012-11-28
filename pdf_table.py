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

def get_page_text(page):
    page_elements = get_page_elements(page)
    istext = lambda el: isinstance(el, LTTextBox) or isinstance(el, LTTextLine)
    text_blocks = filter(istext, page_elements)
    return [line for block in text_blocks for line in block]

def update_line(lines, l, block):    
    """
        appends a text block to a line and updates the dict key so that it contains 
        the average of y0 values for all its elements
    """
    i = len(lines[l])
    lines[l].append(block)
    new_key = (l * i + block.y0) / (i + 1)
    lines[new_key] = lines.pop(l)
    
def compose_lines(text, avg_line_height):
    lines = {}
    for block in text:
        for l in lines:
            if abs(l - block.y0) < avg_line_height * 0.8:
                update_line(lines, l, block)
                break
        else:
            lines[block.y0] = [block]
    return lines

def break_columns(lines):
    pass

if __name__ == "__main__":
    pages = get_doc_pages('/home/ju/Downloads/A_B.pdf')
    page = pages.next() # for i, page in enumerate(pages):
    text = get_page_text(page)
    lines = compose_lines(text, 10.5)
    for line_number in sorted(lines.keys(), reverse=True):
        print "[%s]" % line_number
        for cell in lines[line_number]:
            print cell.get_text()
    print "Total: %s linhas" % (len(lines))
