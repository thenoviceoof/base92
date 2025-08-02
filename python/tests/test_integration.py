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


class TestBase92Integration(unittest.TestCase):
    """Integration tests for base92 base92_encode/decode functions"""

    def test_encode_decode_hello_world(self):
        """Test examples from the module docstring"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                # Test 'hello world' example
                encoded = module.base92_encode(b"hello world")
                self.assertEqual(encoded, b"Fc_$aOTdKnsM*k")
                self.assertEqual(module.base92_decode(encoded), b"hello world")

    def test_encode_decode_binary(self):
        """Test binary data example"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                # Test binary data example
                binary_data = b'^\xb6;\xbb\xe0\x1e\xee\xd0\x93\xcb"\xbb\x8fZ\xcd\xc3'
                encoded_binary = module.base92_encode(binary_data)
                self.assertEqual(encoded_binary, b"C=i.w6'IvB/viUpRAwco")
                # Note: decode returns the escaped string representation
                self.assertEqual(
                    module.base92_decode(encoded_binary),
                    b'^\xb6;\xbb\xe0\x1e\xee\xd0\x93\xcb"\xbb\x8fZ\xcd\xc3',
                )

    def test_regression_test(self):
        """Test the regression case from the docstring"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                test_string = b"aoeuaoeuaoeu"
                self.assertEqual(
                    module.base92_decode(module.base92_encode(test_string)), test_string
                )


class TestBase92Package(unittest.TestCase):
    def test_alias_functions(self):
        """Test that alias function equality"""
        # Only test the main base92 module for alias equality since submodules don't have the same aliasing.
        self.assertEqual(base92.base92_encode, base92.b92encode, base92.encode)
        self.assertEqual(base92.base92_decode, base92.b92decode, base92.decode)


class TestBase92Characters(unittest.TestCase):
    """Test single character encoding/decoding"""

    def test_single_character_strings(self):
        """Test single character encoding/decoding"""
        for module_name, module in MODULES:
            with self.subTest(module_name=module_name):
                for i in range(256):
                    char = bytes([i])
                    encoded = module.base92_encode(char)
                    decoded = module.base92_decode(encoded)
                    self.assertEqual(
                        decoded, char, f"Failed for character {i} ({repr(char)})"
                    )
