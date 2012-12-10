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

def update_key(dic, old_key, new_key):    
    """
        appends a text block to a line and updates the dict key so that it contains 
        the average of y0 values for all its elements
    """
    i = len(dic[old_key])
    avg_key = ((i - 1) * old_key + new_key) / i
    dic[avg_key] = dic.pop(old_key)

def compose_table(text, avg_line_height, avg_col_width):
    lines = {}
    cols = {}

    for block in text:

        # breaks the text in lines using avg y0
        for l in lines:
            if abs(l - block.y0) < avg_line_height * 0.8:
                lines[l].append(block)
                update_key(lines, l, block.y0)
                break
        else:
            lines[block.y0] = [block]
        
        # breaks the text in cols using avg x0
        for c in cols:
            if abs(c - block.x0) < avg_col_width * 0.8:
                cols[c].append(block)
                update_key(cols, c, block.x0)
                break
        else:
            cols[block.x0] = [block]

    return lines, cols

def strip_metadata(text):
    """
    Works only for UERJ grade template specific pdf
    """
    contains = lambda bl, tx: bl.get_text().find(tx) != -1
    not_meta = lambda b: not (contains(b, '/') or contains(b, ':') or contains(b, 'Exame Discursivo') or contains(b, 'Nome do Candidato'))
    return filter(not_meta, text)


if __name__ == "__main__":
    pages = get_doc_pages('/home/ju/Downloads/A_B.pdf')
    page = pages.next() # for i, page in enumerate(pages):
    text = strip_metadata(get_page_text(page))

    lines, cols  = compose_table(text, 11.5, 26.5)
    for line_number in sorted(lines.keys(), reverse=True):
        print "[%.01f]" % line_number
    print "Total: %s linhas" % (len(lines))    
    for col_number in sorted(cols.keys()):
        print "[%.01f]" % col_number
    print "Total: %s colunas" % (len(cols))     
