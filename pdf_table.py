#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reads a pdf document and converts it into a table
"""

from pdfminer.pdfparser import PDFParser, PDFDocument, PDFNoOutlines
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage

def initialize_doc(filename):
	fp = open(filename, 'rb')
	parser = PDFParser(fp)
	doc = PDFDocument()
	parser.set_document(doc)
	doc.set_parser(parser)
	doc.initialize()
	return doc

def read_lines(page):
	rsrcmgr = PDFResourceManager()
	laparams = LAParams()
	device = PDFPageAggregator(rsrcmgr, laparams=laparams)
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	interpreter.process_page(page)
	lines = device.get_result()
	return filter(lambda x: isinstance(x, LTTextBox) or isinstance(x, LTTextLine), lines)

if __name__ == "__main__":
	pages = initialize_doc('/home/ju/Downloads/A_B.pdf').get_pages()
	page = pages.next() # for i, page in enumerate(pages):
	for line in read_lines(page):
		print line
