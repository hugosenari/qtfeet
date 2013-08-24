#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_qtfeet
----------------------------------

Tests for `qtfeet` module.
"""

import unittest

from qtfeet import qtfeet


class TestQtfeet(unittest.TestCase):

    def setUp(self):
        qtfeet.__name__

    def test_something(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
