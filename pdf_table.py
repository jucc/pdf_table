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
    text_blocks = filter(lambda x: isinstance(x, LTTextBox) or isinstance(x, LTTextLine), page_elements)
    return [line for block in text_blocks for line in block]

def compose_lines(text):
    lines = {}
    for block in text:
        found = False
        for l in lines:
            if abs(l - block.y0) < 10:
                lines[l].append(block)
                found = True

        if not found:
            lines[block.y0] = [block]
    return lines

def break_columns(lines):
    pass

if __name__ == "__main__":
    pages = get_doc_pages('/home/ju/Downloads/A_B.pdf')
    page = pages.next() # for i, page in enumerate(pages):
    text = get_page_text(page)
#   for block in text:
#        if 435 <= block.x0 and block.x0  <= 448:
#        if block.y0 > 240 and block.y0 < 242:
#            print "[%s][w=%03f]: %s" % (block.x0, block.x1 - block.x0, block.get_text())
    lines = compose_lines(text)
    for line_number in sorted(lines.keys()):
        print line_number
    print "%s linhas" % (len(lines))
