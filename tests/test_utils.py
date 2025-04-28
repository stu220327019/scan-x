import unittest
from lib.utils import *

class TestUtils(unittest.TestCase):
    def test_sizeof_fmt(self):
        self.assertEqual(sizeof_fmt(2585483940), '2.41 GB')
