#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from pdf import *
from table import *
from grades import *
import unittest

class TestPdfToTable(unittest.TestCase):

    def setUp(self):
        self.pdf = ('/home/ju/Downloads/A_B.pdf')
        self.block = Block(42, 42, 'ju')

        self.lines = [10, 20]
        self.cols=[0, 10, 20, 30]
        self.blocks = []
        self.blocks.append(Block(0, 10, 'ju'))
        self.blocks.append(Block(10, 20, '10'))
        self.blocks.append(Block(0, 20, 'ronald'))
        self.blocks.append(Block(10, 10, '9'))
        self.blocks.append(Block(20, 10, '9'))
        self.blocks.append(Block(30, 20, '10'))
  
        self.line_ju = ['ju', None, None, None, None, None, None, 8.5, 5.5, 8]
        self.line_ron = ['ronald', None, None, None, None, None, 10, 10, None, 10]

    def test_doc_has_pages(self):
        self.assertIsNotNone(get_doc_pages(self.pdf))


    def test_inside_partition(self):
        self.assertTrue(self.block.belongs_to_line(39))

    def test_outside_partition(self):
        self.assertFalse(self.block.belongs_to_column(17))

    def test_update_avg(self):
        l = [17, 35, 14]
        self.assertEquals(27, update_average(22, 3, 42))


    def test_find_blocks(self):
        pages = get_doc_pages(self.pdf)
        text = extract_text_elements(pages.next())
        blocks = Block.strip_metadata(Block.convert_to_blocks(text))
        pos = find_partitions(blocks)
        self.assertEquals(63, len(pos[0]))
        self.assertEquals(10, len(pos[1]))

    def test_blocks_to_cells(self):
        blocks = self.blocks
        expected = [['ju', 9, 9, None], ['ronald', 10, None, 10]]
        result = assemble_table(blocks)
        self.assertEquals(expected, result)

    def test_get_chem_eng(self):
        lines = [self.line_ju, self.line_ron]
        result = get_chem_eng(lines)
        self.assertEquals([self.line_ju], result)        

    def test_get_grade(self):
        weights = {7:2, 8:1, 9:1}
        result = get_grade(self.line_ju, weights)
        self.assertEquals(40.1, result)
        

if __name__ == '__main__':
    unittest.main()

