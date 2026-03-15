import os
import sys
import unittest

# make src importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from int_to_roman import int_to_roman


class TestIntToRoman(unittest.TestCase):
    def test_various_numbers(self):
        cases = {
            1: 'I',
            4: 'IV',
            9: 'IX',
            58: 'LVIII',
            1994: 'MCMXCIV',
        }
        for n, expected in cases.items():
            with self.subTest(n=n):
                self.assertEqual(int_to_roman(n), expected)

