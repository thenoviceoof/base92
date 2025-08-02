# Copyright 2025 Nathan Hwang, thenoviceoof
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the “Software”), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
base92: a library for encoding byte strings
"""

import math

_BASE92_CHARS = (
    [ord("!")] + [ord("#") + i for i in range(61)] + [ord("a") + i for i in range(29)]
)
_BASE92_VALUES = {char: idx for idx, char in enumerate(_BASE92_CHARS)}


def base92_chr(val: int) -> int:
    """
    Map an integer value in the range [0, 91) to a character.
    """
    if val < 0 or val >= 91:
        raise ValueError("Unexpected base92 encoding failure")
    return _BASE92_CHARS[val]


def base92_ord(val: int) -> int:
    """
    Map a base92 character to an integer.
    """
    try:
        return _BASE92_VALUES[val]
    except KeyError:
        raise ValueError("Invalid base92 character")


def base92_encode(bytstr: bytes) -> bytes:
    """
    Take a byte string, and encode it in base 92.
    """
    if not bytstr:
        return b"~"

    # Convert bytes to a single integer for bitwise processing
    bit_buffer = 0
    bit_count = 0
    result = bytearray()

    for byte in bytstr:
        bit_buffer = (bit_buffer << 8) | byte
        bit_count += 8

        # Process 13-bit chunks
        while bit_count >= 13:
            # Extract top 13 bits
            chunk = bit_buffer >> (bit_count - 13)
            bit_buffer &= (1 << (bit_count - 13)) - 1  # Keep remaining bits
            bit_count -= 13

            # Encode as two base92 characters
            result.append(base92_chr(chunk // 91))
            result.append(base92_chr(chunk % 91))

    # Handle remaining bits
    if bit_count > 0:
        if bit_count < 7:
            # Pad to 6 bits and encode as single character
            chunk = bit_buffer << (6 - bit_count)
            result.append(_BASE92_CHARS[chunk])
        else:
            # Pad to 13 bits and encode as two characters
            chunk = bit_buffer << (13 - bit_count)
            result.append(_BASE92_CHARS[chunk // 91])
            result.append(_BASE92_CHARS[chunk % 91])

    return bytes(result)


def base92_decode(bstr: bytes) -> bytes:
    """
    Take a base92 encoded string, convert it back to a byte string.
    """
    if bstr == b"~":
        return b""

    if len(bstr) == 1:
        raise ValueError("1 character is not a valid base92 encoding")

    bit_buffer = 0
    bit_count = 0
    result = bytearray()

    # Process pairs of characters
    i = 0
    while i < len(bstr) - 1:
        # Decode pair to 13-bit value
        val1 = base92_ord(bstr[i])
        val2 = base92_ord(bstr[i + 1])

        chunk = val1 * 91 + val2
        if chunk >= 8192:
            raise ValueError("Invalid base92 string")
        bit_buffer = (bit_buffer << 13) | chunk
        bit_count += 13

        # Extract complete bytes
        while bit_count >= 8:
            byte_val = bit_buffer >> (bit_count - 8)
            result.append(byte_val)
            bit_buffer &= (1 << (bit_count - 8)) - 1
            bit_count -= 8

        i += 2

    # Handle single remaining character
    if i < len(bstr):
        val = base92_ord(bstr[i])

        bit_buffer = (bit_buffer << 6) | val
        bit_count += 6

        # Extract any complete bytes
        # We pad the encoding, and each encoded character is smaller
        # than a byte, so any leftover bits are safe to throw away.
        while bit_count >= 8:
            byte_val = bit_buffer >> (bit_count - 8)
            result.append(byte_val)
            bit_buffer &= (1 << (bit_count - 8)) - 1
            bit_count -= 8

    return bytes(result)
