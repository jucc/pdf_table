#!usr/bin/env python
# -*- coding: utf-8 -*-

from pdf import *
from table import *
from grades import *

pages = get_doc_pages('/home/ju/Downloads/A_B.pdf')
page = pages.next()
text = extract_text_elements(page)
blocks = Block.strip_metadata(Block.convert_to_blocks(text))
table = assemble_table(blocks)
for line in table:
    print line
