import os
import platform
import sys
import unittest

import base92
from base92 import _base92python

MODULES = [
    ("base92._base92python", _base92python),
]
# If we're running tests under pypy or some other Python, don't try to
# test the nonexistent compiled version.
if platform.python_implementation() == "CPython":
    from base92 import _base92compiled

    MODULES.append(("base92._base92compiled", _base92compiled))


class TestBase92Encode(unittest.TestCase):
    """Test cases for base92_encode function"""

    def test_base92_encode_empty_string(self):
        """Test encoding empty string"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_encode(b""), b"~")

    def test_base92_encode_single_bytes(self):
        """Test encoding single byte values"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_encode(b"\x00"), b"!!")
                self.assertEqual(module.base92_encode(b"\x01"), b"!B")
                self.assertEqual(module.base92_encode(b"\xff"), b"|_")

    def test_base92_base92_encode_multi_bytes(self):
        """Test encoding multiple byte values"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_encode(b"aa"), b"D8*")
                self.assertEqual(
                    module.base92_encode(b"aaaaaaaaaaaaa"), b"D81RPya.)hgNA(%s"
                )


class TestBase92Decode(unittest.TestCase):
    """Test cases for base92_decode function"""

    def test_base92_decode_invalid_chars(self):
        """Test base92_decode with invalid characters"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                with self.assertRaises(ValueError) as cm:
                    module.base92_decode(b"aa ")
                self.assertEqual(str(cm.exception), "Invalid base92 character")

    def test_base92_decode_length(self):
        """Test base92_decode with invalid length strings"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                with self.assertRaises(ValueError) as cm:
                    module.base92_decode(b"a")
                self.assertEqual(
                    str(cm.exception), "1 character is not a valid base92 encoding"
                )

    def test_base92_decode_invalid_string(self):
        """Test base92_decode with an invalid string"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                with self.assertRaises(ValueError) as cm:
                    module.base92_decode(b"}$")
                self.assertEqual(str(cm.exception), "Invalid base92 string")

    def test_base92_decode_empty_string(self):
        """Test decoding empty string"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_decode(b""), b"")
                self.assertEqual(module.base92_decode(b"~"), b"")

    def test_base92_decode_single_bytes(self):
        """Test decoding to single byte values"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_decode(b"!!"), b"\x00")
                self.assertEqual(module.base92_decode(b"!B"), b"\x01")
                self.assertEqual(module.base92_decode(b"|_"), b"\xff")

    def test_base92_decode_multi_bytes(self):
        """Test decoding to multiple byte values"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_decode(b"D8*"), b"aa")
                self.assertEqual(
                    module.base92_decode(b"D81RPya.)hgNA(%s"), b"aaaaaaaaaaaaa"
                )
