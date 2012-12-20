#!usr/bin/env python
# -*- coding: utf-8 -*-

from pdf import *
from table import *
from grades import *
import sys
from os import listdir


def candidates_on_page(page):
    cands_in_page = []
    text = extract_text_elements(page)
    blocks = Block.strip_metadata(Block.convert_to_blocks(text))
    table = assemble_table(blocks)
    return get_chem_eng(table)


def candidates_on_pdf(pdf):
    cands_in_pdf = []
    pages = get_doc_pages(pdf)
    for page in pages:
        cands_in_pdf.extend(candidates_on_page(page))
    return cands_in_pdf


chem_candidates = []
dirname = sys.argv[1]

pdfs = map(lambda x: dirname + '/' + x, listdir(dirname))

for pdf in pdfs:
    print "-----Parsing %s-----" % pdf
    chem_candidates.extend(candidates_on_pdf(pdf))    
     
rank(chem_candidates)

for i, line in enumerate(chem_candidates):
    print "[%i: %s] %.02f" % (i+1, line[0], line[-1])
