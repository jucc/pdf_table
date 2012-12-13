#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extracts text elements (with text, position and dimensions) from a table
Reference for pdfminer work: http://denis.papathanasiou.org/?tag=pdfminer
Meant to be used together with blocks.py, which converts the elements in a table
"""

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

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

def extract_text_elements(page):
    """
    Filters the elements that contain text (as opposed to images, etc) 
    and extracts the textlines into the constituting textblocks 
    """
    page_elements = get_page_elements(page)
    istext = lambda el: isinstance(el, LTTextBox) or isinstance(el, LTTextLine)
    text = filter(istext, page_elements)
    return [tb for boxes in text for tb in boxes]


if __name__ == "__main__":
    pages = get_doc_pages('/home/ju/Downloads/A_B.pdf')
    for i, page in enumerate(pages):
        text = extract_text_elements(page)
        print "page %s has %s text blocks" % (i, len(text))   
