import os
import platform
import sys
import unittest

import base92
from base92 import _base92python, _base92compiled

MODULES = [
    ("base92._base92python", _base92python),
]
# If we're running tests under pypy or some other Python, don't try to
# test the nonexistent compiled version.
if platform.python_implementation() == "CPython":
    MODULES.append(("base92._base92compiled", _base92compiled))


# Chr/Ord functions aren't defined for the C extension, so we can only test it for the pure python version.
class TestBase92Chr(unittest.TestCase):
    """Test cases for base92_chr function"""

    def test_base92_chr_valid_values(self):
        """Test base92_chr with valid input values"""
        self.assertEqual(_base92python.base92_chr(0), "!")
        self.assertEqual(_base92python.base92_chr(1), "#")
        self.assertEqual(_base92python.base92_chr(61), "_")
        self.assertEqual(_base92python.base92_chr(62), "a")
        self.assertEqual(_base92python.base92_chr(90), "}")

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
        self.assertEqual(_base92python.base92_ord("!"), 0)
        self.assertEqual(_base92python.base92_ord("#"), 1)
        self.assertEqual(_base92python.base92_ord("_"), 61)
        self.assertEqual(_base92python.base92_ord("a"), 62)
        self.assertEqual(_base92python.base92_ord("}"), 90)

    def test_base92_ord_invalid_chars(self):
        """Test base92_ord with invalid characters"""
        with self.assertRaises(ValueError) as cm:
            _base92python.base92_ord(" ")
        self.assertEqual(str(cm.exception), "Invalid base92 character")


class TestBase92Encode(unittest.TestCase):
    """Test cases for base92_encode function"""

    def test_base92_encode_empty_string(self):
        """Test encoding empty string"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_encode(b""), "~")

    def test_base92_encode_single_bytes(self):
        """Test encoding single byte values"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_encode(b"\x00"), "!!")
                self.assertEqual(module.base92_encode(b"\x01"), "!B")
                self.assertEqual(module.base92_encode(b"\xff"), "|_")

    def test_base92_base92_encode_multi_bytes(self):
        """Test encoding multiple byte values"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_encode(b"aa"), "D8*")
                self.assertEqual(
                    module.base92_encode(b"aaaaaaaaaaaaa"), "D81RPya.)hgNA(%s"
                )


class TestBase92Decode(unittest.TestCase):
    """Test cases for base92_decode function"""

    def test_base92_decode_invalid_chars(self):
        """Test base92_ord with invalid characters"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                with self.assertRaises(ValueError) as cm:
                    module.base92_decode("aa ")
                self.assertEqual(str(cm.exception), "Invalid base92 character")

    def test_base92_decode_length(self):
        """Test base92_ord with invalid characters"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                with self.assertRaises(ValueError) as cm:
                    module.base92_decode("a")
                self.assertEqual(
                    str(cm.exception), "1 character is not a valid base92 encoding"
                )

    def test_base92_decode_empty_string(self):
        """Test decoding empty string"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_decode(""), b"")
                self.assertEqual(module.base92_decode("~"), b"")

    def test_base92_decode_single_bytes(self):
        """Test decoding to single byte values"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_decode("!!"), b"\x00")
                self.assertEqual(module.base92_decode("!B"), b"\x01")
                self.assertEqual(module.base92_decode("|_"), b"\xff")

    def test_base92_decode_multi_bytes(self):
        """Test decoding to multiple byte values"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                self.assertEqual(module.base92_decode("D8*"), b"aa")
                self.assertEqual(
                    module.base92_decode("D81RPya.)hgNA(%s"), b"aaaaaaaaaaaaa"
                )


class TestBase92Integration(unittest.TestCase):
    """Integration tests for base92 base92_encode/decode functions"""

    def test_encode_decode_hello_world(self):
        """Test examples from the module docstring"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                # Test 'hello world' example
                encoded = module.base92_encode(b"hello world")
                self.assertEqual(encoded, "Fc_$aOTdKnsM*k")
                self.assertEqual(module.base92_decode(encoded), b"hello world")

    def test_encode_decode_binary(self):
        """Test binary data example"""
        for module_name, module in MODULES:
            with self.subTest(module=module_name):
                # Test binary data example
                binary_data = b'^\xb6;\xbb\xe0\x1e\xee\xd0\x93\xcb"\xbb\x8fZ\xcd\xc3'
                encoded_binary = module.base92_encode(binary_data)
                self.assertEqual(encoded_binary, "C=i.w6'IvB/viUpRAwco")
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
