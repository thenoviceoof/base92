import os
import platform
import sys
import unittest

import base92
from base92 import _base92python


# Chr/Ord functions aren't defined for the C extension, so we can only test it for the pure python version.
class TestBase92Chr(unittest.TestCase):
    """Test cases for base92_chr function"""

    def test_base92_chr_valid_values(self):
        """Test base92_chr with valid input values"""
        self.assertEqual(_base92python.base92_chr(0), ord("!"))
        self.assertEqual(_base92python.base92_chr(1), ord("#"))
        self.assertEqual(_base92python.base92_chr(61), ord("_"))
        self.assertEqual(_base92python.base92_chr(62), ord("a"))
        self.assertEqual(_base92python.base92_chr(90), ord("}"))

    def test_base92_chr_invalid_values(self):
        """Test base92_chr with invalid input values"""
        with self.assertRaises(ValueError) as cm:
            _base92python.base92_chr(91)
        self.assertEqual(str(cm.exception), "Unexpected base92 encoding failure")

        with self.assertRaises(ValueError) as cm:
            _base92python.base92_chr(-1)
        self.assertEqual(str(cm.exception), "Unexpected base92 encoding failure")


class TestBase92Ord(unittest.TestCase):
    """Test cases for base92_ord function"""

    def test_base92_ord_valid_chars(self):
        """Test base92_ord with valid characters"""
        self.assertEqual(_base92python.base92_ord(ord("!")), 0)
        self.assertEqual(_base92python.base92_ord(ord("#")), 1)
        self.assertEqual(_base92python.base92_ord(ord("_")), 61)
        self.assertEqual(_base92python.base92_ord(ord("a")), 62)
        self.assertEqual(_base92python.base92_ord(ord("}")), 90)

    def test_base92_ord_invalid_chars(self):
        """Test base92_ord with invalid characters"""
        with self.assertRaises(ValueError) as cm:
            _base92python.base92_ord(ord(" "))
        self.assertEqual(str(cm.exception), "Invalid base92 character")
