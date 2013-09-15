#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from tests.test_qtfeet import TestQtfeet  # lint:ok


def tests_main():
    TestQtfeet
    unittest.main()

# Classic...
if __name__ == "__main__":
    tests_main()
