#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import conf
conf.use_fix_columns = False
from pdf import *
from table import *
from grades import *
import unittest

class TestPdfToTable(unittest.TestCase):

    def setUp(self):
        conf.use_fix_columns = False
        self.pdf = ('pdf2012/A_B.pdf')
        self.block = Block(42, 42, 'ju')
        self.block2 = Block(54, 10, '9')
        self.lines = [10, 22]
        self.cols = [0, 27, 54, 81]
        self.blocks = []
        self.blocks.append(Block(0, 10, 'JU'))
        self.blocks.append(Block(27, 0, '10'))
        self.blocks.append(Block(0, 0, 'RONALD'))
        self.blocks.append(Block(54, 22, 'header'))
        self.blocks.append(Block(27, 10, '9'))
        self.blocks.append(Block(54, 10, '9,5 10'))
        self.blocks.append(Block(81, 0, '10'))
  
        self.line_ju = ['JU', None, None, None, None, None, None, 11.0, 17.0, 15.5]
        self.line_ron = ['RONALD', None, None, None, None, None, 18.0, 17.0, None, 16.0]

    def test_doc_has_pages(self):
        self.assertIsNotNone(get_doc_pages(self.pdf))


    def test_inside_partition(self):
        self.assertTrue(self.block.belongs_to_line(39))

    def test_outside_partition(self):
        self.assertFalse(self.block.belongs_to_column(17))

    def test_update_avg(self):
        l = [17, 35, 14]
        self.assertEquals(27, update_average(22, 3, 42))

    def test_find_line(self):
        result = self.block2.find_line(self.lines)
        self.assertEquals(0, result)

    def test_find_col(self):        
        result = self.block2.find_col(self.cols)
        self.assertEquals(2, result)

    def test_find_pos(self):
        result = self.block2.find_position(self.lines, self.cols)
        self.assertEquals((0, 2), result) 

    def test_find_blocks(self):
        pages = get_doc_pages(self.pdf)
        text = extract_text_elements(pages.next())
        blocks = Block.strip_metadata(Block.convert_to_blocks(text))
        pos = find_partitions(blocks)
        self.assertEquals(63, len(pos[0]))
        self.assertEquals(10, len(pos[1]))

    def test_empty_table(self):
        expected = [[None, None], [None, None], [None, None]]
        result = empty_table(3, 2)
        self.assertEquals(expected, result)

    def test_empty_table_passing_list(self):
        expected = [[None, None], [None, None], [None, None]]
        result = empty_table(range(3), range(2))
        self.assertEquals(expected, result)

    def test_get_name(self):
        col = '12345-6 JULIANA CAVALCANTI CORREA'
        result = get_name(col)
        self.assertEquals('JULIANA CAVALCANTI CORREA', result)

    def test_blocks_to_lines(self):
        blocks = self.blocks
        expected = [['JU', '9', '9.5', '10'], ['RONALD', '10', None, '10']]
        b = Block.strip_metadata(blocks)
        result = assemble_table(b)
        self.assertEquals(expected, result)

    def test_get_chem_eng(self):
        lines = [self.line_ju, self.line_ron]
        result = get_chem_eng(lines)
        self.assertEquals([self.line_ju], result)        

    def test_get_grade(self):
        result = get_grade(self.line_ju)
        self.assertEquals(60.5, result)
        
    def test_grade_students(self):
        lines = [self.line_ju[:], self.line_ju[:], self.line_ju[:]]
        grade_students(lines)
        expected = self.line_ju[:]
        expected.append(60.5)
        self.assertEquals([expected, expected, expected], lines)

    def test_sort_grades(self):
        graded_lines = [
            ['ju1', None, None, None, None, None, None, 10, 9, 10, 80.5],
            ['ju2', None, None, None, None, None, None, 10, 10, 10, 100],
            ['ju3', None, None, None, None, None, None, 10, 10, 10, 0.0],
            ['ju4', None, None, None, None, None, None, 10, 10, 10, 80.5],
            ['ju5', None, None, None, None, None, None, 9, 10, 10, 80.5],
        ]
        sort_grades(graded_lines)
        expected = [
            ['ju2', None, None, None, None, None, None, 10, 10, 10, 100],
            ['ju4', None, None, None, None, None, None, 10, 10, 10, 80.5],
            ['ju5', None, None, None, None, None, None, 9, 10, 10, 80.5],
            ['ju1', None, None, None, None, None, None, 10, 9, 10, 80.5],
            ['ju3', None, None, None, None, None, None, 10, 10, 10, 0.0],
        ]
        self.assertEquals(expected, graded_lines)


    def test_qualifying_exam(self):
        pages = get_doc_pages('qual2012/A_B.pdf')
        page = pages.next()
        text = extract_text_elements(page)
        blocks = Block.strip_metadata(Block.convert_to_blocks(text))
        table = assemble_table(blocks)
        self.assertEquals(3, len(table[0]))

        
    def test_get_lines(self):
        pages = get_doc_pages(self.pdf)
        text = extract_text_elements(pages.next())
        blocks = Block.strip_metadata(Block.convert_to_blocks(text))
        res = find_lines(blocks)
        self.assertEquals(67, len(res))


if __name__ == '__main__':
    unittest.main()

