#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from pdf import *
from table import *
import unittest

class TestGetTableFromPdf(unittest.TestCase):

    def setUp(self):
        self.pdf = ('/home/ju/Downloads/A_B.pdf')
        self.block = Block(42, 42, 'ju')

    def test_doc_has_pages(self):
        self.assertIsNotNone(get_doc_pages(self.pdf))

    def test_inside_partition(self):
        self.assertTrue(self.block.belongs_to_line(39))

    def test_outside_partition(self):
        self.assertFalse(self.block.belongs_to_column(17))

    def test_update_avg(self):
        l = [17, 35, 14]
        avg = sum(l) / len(l)
        self.assertEquals(27, update_average(22, 3, 42))

    def test_find_blocks(self):
        pages = get_doc_pages(self.pdf)
        text = extract_text_elements(pages.next())
        blocks = Block.strip_metadata(Block.convert_to_blocks(text))
        pos = find_partitions(blocks)
        self.assertEquals(63, len(pos[0]))
        self.assertEquals(10, len(pos[1]))

    def test_convert_blocks_to_cells(self):
        lines = [10, 20]
        cols=[0, 10, 20, 30]
        blocks = []
        blocks.append(Block(0, 10, 'ju'))
        blocks.append(Block(0, 20, 'ronald'))
        blocks.append(Block(10, 10, '9'))
        blocks.append(Block(10, 20, '10'))
        blocks.append(Block(20, 10, '7'))
        blocks.append(Block(30, 20, '8'))
    
        expected = [['ju', 9, 7, None], ['ronald', 10, None, 8]]
        result = sort_table(blocks, lines, cols)
        self.assertEquals(expected, result)

    def test_get_grade(self):
        line = ['ju', 10, None, 9, 8, None, None]
        weights = {1:2, 3:1, 4:1}
        expected = (10 * 2 + 9 + 8) / 4
        result = get_grade(line, weights)
        self.assertEquals(expected, result)
        

if __name__ == '__main__':
    unittest.main()

