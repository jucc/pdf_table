#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from pdf_table import *
import unittest


class Mock_block:
    def __init__(self, x, y, tx):
        self.x0 = x
        self.y0 = y
        self.text = tx

    def getText(self):
        return self.text

class TestGetTableFromPdf(unittest.TestCase):

    def setUp(self):
        self.pdf = ('/home/ju/Downloads/A_B.pdf')

    def test_doc_has_pages(self):
        self.assertIsNotNone(get_doc_pages(self.pdf))

    def test_inside_partition(self):
        self.assertTrue(belongs_to_partition(35, 42, 17))

    def test_outside_partition(self):
        self.assertFalse(belongs_to_partition(17, 42, 17))

    def test_update_avg(self):
        l = [17, 35, 14]
        avg = sum(l) / len(l)
        self.assertEquals(27, update_average(22, 3, 42))

    def test_find_blocks(self):
        pages = get_doc_pages(self.pdf)
        text = strip_metadata(get_text_elements(pages.next()))
        blocks = find_blocks(text, 11.5, 26.5)
        self.assertEquals(63, len(blocks[0]))
        self.assertEquals(10, len(blocks[1]))

    def test_convert_blocks_to_cells(self):
        lines = [10, 20]
        cols=[0, 10, 20, 30]
        a = []
        a.append(Mock_block(0, 10, 'ju'))
        a.append(Mock_block(0, 20, 'ronald'))
        a.append(Mock_block(10, 10, '9'))
        a.append(Mock_block(10, 20, '10'))
        a.append(Mock_block(20, 10, '7'))
        a.append(Mock_block(30, 20, '8'))
    
        expected = [['ju', 9, 7, None], ['ronald', 10, None, 8]]
        result = create_table(a, lines, cols)
        self.assertEquals(expected, result)

    def test_get_grade(self):
        line = ['ju', 10, None, 9, 8, None, None]
        pesos = {1:2, 3:1, 4:1}
        expected = (10 * 2 + 9 + 8) / 4
        result = get_grade(line, pesos)
        self.assertEquals(expected, result)
        

if __name__ == '__main__':
    unittest.main()

