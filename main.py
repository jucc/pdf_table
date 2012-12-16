#!usr/bin/env python
# -*- coding: utf-8 -*-

from pdf import *
from table import *
from grades import *

chem_candidates = []
pages = get_doc_pages('/home/ju/Downloads/A_B.pdf')
for page in pages:
    text = extract_text_elements(page)
    blocks = Block.strip_metadata(Block.convert_to_blocks(text))
    table = assemble_table(blocks)
    chem_candidates.extend(get_chem_eng(table))
    print len(chem_candidates)

for line in chem_candidates:
    print line
