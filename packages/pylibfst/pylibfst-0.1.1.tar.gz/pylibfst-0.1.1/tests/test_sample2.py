'''Test wal eval logic'''
import unittest
import random

# pylint: disable=C0103
# _pylint: disable=W0201

class BasicOpTest(unittest.TestCase):
    '''Test built-in functions'''

    def setUp(self):
        print("setup")
        self.assertEqual(1, 1)

    def dummysubtest(self):
        print("dummy ok")
