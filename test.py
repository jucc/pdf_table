#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from pdf_table import *
import unittest

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

if __name__ == '__main__':
    unittest.main()
