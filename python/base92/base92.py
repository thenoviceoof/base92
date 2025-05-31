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

__version__ = (1, 0, 3)


def base92_chr(val: int) -> str:
    """
    Map an integer value in the range [0, 91) to a character.
    """
    if val < 0 or val >= 91:
        raise ValueError("val must be in [0, 91)")
    if val == 0:
        return "!"
    elif val <= 61:
        return chr(ord("#") + val - 1)
    else:
        return chr(ord("a") + val - 62)


def base92_ord(val: str) -> int:
    """
    Map a base92 character to an integer.
    """
    num = ord(val)
    if val == "!":
        return 0
    elif ord("#") <= num and num <= ord("_"):
        return num - ord("#") + 1
    elif ord("a") <= num and num <= ord("}"):
        return num - ord("a") + 62
    else:
        raise ValueError("val is not a base92 character")


def base92_encode(bytstr: bytes) -> str:
    """
    Take a byte string, and encode it in base 92.
    """
    # Always encode *something*, in case we need to avoid empty strings
    if not bytstr:
        return "~"
    # Prime the pump.
    bitstr = ""
    while len(bitstr) < 13 and bytstr:
        bitstr += "{:08b}".format(bytstr[0])
        bytstr = bytstr[1:]
    resstr = ""
    while len(bitstr) > 13 or bytstr:
        i = int(bitstr[:13], 2)
        resstr += base92_chr(i // 91)
        resstr += base92_chr(i % 91)
        bitstr = bitstr[13:]
        while len(bitstr) < 13 and bytstr:
            bitstr += "{:08b}".format(bytstr[0])
            bytstr = bytstr[1:]
    if bitstr:
        if len(bitstr) < 7:
            bitstr += "0" * (6 - len(bitstr))
            resstr += base92_chr(int(bitstr, 2))
        else:
            bitstr += "0" * (13 - len(bitstr))
            i = int(bitstr, 2)
            resstr += base92_chr(i // 91)
            resstr += base92_chr(i % 91)
    return resstr


def base92_decode(bstr: str) -> bytes:
    """
    Take a base92 encoded string, convert it back to a byte string.
    """
    bitstr = ""
    resstr = b""
    if bstr == "~":
        return resstr
    # we always have pairs of characters
    for i in range(len(bstr) // 2):
        x = base92_ord(bstr[2 * i]) * 91 + base92_ord(bstr[2 * i + 1])
        bitstr += "{:013b}".format(x)
        while 8 <= len(bitstr):
            resstr += bytes([int(bitstr[0:8], 2)])
            bitstr = bitstr[8:]
    # if we have an extra char, check for extras
    if len(bstr) % 2 == 1:
        x = base92_ord(bstr[-1])
        bitstr += "{:06b}".format(x)
        while 8 <= len(bitstr):
            resstr += bytes([int(bitstr[0:8], 2)])
            bitstr = bitstr[8:]
    return resstr


encode = base92_encode
b92encode = base92_encode

decode = base92_decode
b92decode = base92_decode

## size tests
# import base64
# import base85
# from pprint import pprint
# sd = [(len(base64.b64encode('a'*i)),
#        len(base85.b85encode('a'*i)),
#        len(encode('a'*i)))
#       for i in range(1,128)]
# pprint(sd)
# print sum(a-c for a,b,c in sd)/float(len(sd))
# print sum(b-c for a,b,c in sd)/float(len(sd))
