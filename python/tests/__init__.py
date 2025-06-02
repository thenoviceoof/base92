import unittest
import sys
import os

from base92 import base92


class TestBase92Chr(unittest.TestCase):
    """Test cases for base92_chr function"""

    def test_base92_chr_valid_values(self):
        """Test base92_chr with valid input values"""
        self.assertEqual(base92.base92_chr(0), "!")
        self.assertEqual(base92.base92_chr(1), "#")
        self.assertEqual(base92.base92_chr(61), "_")
        self.assertEqual(base92.base92_chr(62), "a")
        self.assertEqual(base92.base92_chr(90), "}")

    def test_base92_chr_invalid_values(self):
        """Test base92_chr with invalid input values"""
        with self.assertRaises(ValueError) as cm:
            base92.base92_chr(91)
        self.assertEqual(str(cm.exception), "val must be in [0, 91)")

        with self.assertRaises(ValueError) as cm:
            base92.base92_chr(-1)
        self.assertEqual(str(cm.exception), "val must be in [0, 91)")


class TestBase92Ord(unittest.TestCase):
    """Test cases for base92_ord function"""

    def test_base92_ord_valid_chars(self):
        """Test base92_ord with valid characters"""
        self.assertEqual(base92.base92_ord("!"), 0)
        self.assertEqual(base92.base92_ord("#"), 1)
        self.assertEqual(base92.base92_ord("_"), 61)
        self.assertEqual(base92.base92_ord("a"), 62)
        self.assertEqual(base92.base92_ord("}"), 90)

    def test_base92_ord_invalid_chars(self):
        """Test base92_ord with invalid characters"""
        with self.assertRaises(ValueError) as cm:
            base92.base92_ord(" ")
        self.assertEqual(str(cm.exception), "val is not a base92 character")


class TestBase92Encode(unittest.TestCase):
    """Test cases for base92_encode function"""

    def test_base92_encode_empty_string(self):
        """Test encoding empty string"""
        self.assertEqual(base92.base92_encode(b""), "~")

    def test_base92_encode_single_bytes(self):
        """Test encoding single byte values"""
        self.assertEqual(base92.base92_encode(b"\x00"), "!!")
        self.assertEqual(base92.base92_encode(b"\x01"), "!B")
        self.assertEqual(base92.base92_encode(b"\xff"), "|_")

    def test_base92_encode_multi_bytes(self):
        """Test encoding multiple byte values"""
        self.assertEqual(base92.base92_encode(b"aa"), "D8*")
        self.assertEqual(base92.base92_encode(b"aaaaaaaaaaaaa"), "D81RPya.)hgNA(%s")


class TestBase92Decode(unittest.TestCase):
    """Test cases for base92_decode function"""

    def test_base92_decode_empty_string(self):
        """Test decoding empty string"""
        self.assertEqual(base92.base92_decode(""), b"")
        self.assertEqual(base92.base92_decode("~"), b"")

    def test_base92_decode_single_bytes(self):
        """Test decoding to single byte values"""
        self.assertEqual(base92.base92_decode("!!"), b"\x00")
        self.assertEqual(base92.base92_decode("!B"), b"\x01")
        self.assertEqual(base92.base92_decode("|_"), b"\xff")

    def test_base92_decode_multi_bytes(self):
        """Test decoding to multiple byte values"""
        self.assertEqual(base92.base92_decode("D8*"), b"aa")
        self.assertEqual(base92.base92_decode("D81RPya.)hgNA(%s"), b"aaaaaaaaaaaaa")


class TestBase92Integration(unittest.TestCase):
    """Integration tests for base92 encode/decode functions"""

    def test_encode_decode_hello_world(self):
        """Test examples from the module docstring"""
        # Test 'hello world' example
        encoded = base92.encode(b"hello world")
        self.assertEqual(encoded, "Fc_$aOTdKnsM*k")
        self.assertEqual(base92.decode(encoded), b"hello world")

    def test_encode_decode_binary(self):
        # Test binary data example
        binary_data = b'^\xb6;\xbb\xe0\x1e\xee\xd0\x93\xcb"\xbb\x8fZ\xcd\xc3'
        encoded_binary = base92.encode(binary_data)
        self.assertEqual(encoded_binary, "C=i.w6'IvB/viUpRAwco")
        # Note: decode returns the escaped string representation
        self.assertEqual(
            base92.decode(encoded_binary),
            b'^\xb6;\xbb\xe0\x1e\xee\xd0\x93\xcb"\xbb\x8fZ\xcd\xc3',
        )

    def test_regression_test(self):
        """Test the regression case from the docstring"""
        test_string = b"aoeuaoeuaoeu"
        self.assertEqual(base92.decode(base92.encode(test_string)), test_string)


class TestBase92Package(unittest.TestCase):
    def test_alias_functions(self):
        """Test that alias function equality"""

        # Test encode aliases
        self.assertEqual(base92.encode, base92.b92encode)

        # Test decode aliases
        self.assertEqual(base92.decode, base92.b92decode)


class TestBase92Characters(unittest.TestCase):
    def test_single_character_strings(self):
        """Test single character encoding/decoding"""
        for i in range(256):
            char = bytes([i])
            encoded = base92.encode(char)
            decoded = base92.decode(encoded)
            self.assertEqual(decoded, char, f"Failed for character {i} ({repr(char)})")
