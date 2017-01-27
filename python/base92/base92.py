# THE BEERWARE LICENSE (Revision 42):
# <thenoviceoof> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer in return
# - Nathan Hwang (thenoviceoof)


"""
base92: a library for encoding byte strings

>>> x = encode(b'hello world')
>>> x
'Fc_$aOTdKnsM*k'
>>> decode(x)
'hello world'

>>> y = encode(b'^\xb6;\xbb\xe0\x1e\xee\xd0\x93\xcb"\xbb\x8fZ\xcd\xc3')
>>> y
"C=i.w6'IvB/viUpRAwco"
>>> decode(y)
'^\\xb6;\\xbb\\xe0\\x1e\\xee\\xd0\\x93\\xcb"\\xbb\\x8fZ\\xcd\\xc3'

this is a regression test
>>> decode(encode('aoeuaoeuaoeu'))
'aoeuaoeuaoeu'
"""

__version__ = (1, 0, 3)

__all__ = [
    'encode',
    'decode',
    'b92encode',
    'b92decode',
    'base92encode',
    'base92decode',
]


if bytes is str:
    _chr = chr
    _ord = ord
else:
    import struct
    _chr = struct.Struct(">B").pack
    _ord = lambda v: v if isinstance(v, int) else ord(v)
    del struct


def base92_chr(val):
    """
    Map an integer value <91 to a char

    >>> base92_chr(0)
    '!'
    >>> base92_chr(1)
    '#'
    >>> base92_chr(61)
    '_'
    >>> base92_chr(62)
    'a'
    >>> base92_chr(90)
    '}'
    >>> base92_chr(91)
    Traceback (most recent call last):
        ...
    ValueError: val must be in [0, 91)
    """
    if val < 0 or val >= 91:
        raise ValueError('val must be in [0, 91)')
    if val == 0:
        return 33  # b'!'  # 33 == ord('!')
    elif val <= 61:
        return 35 + val - 1  # 35 == ord('#')
    else:
        return 97 + val - 62  # 97 == ord('a')

    
def base92_ord(val, _excl=_ord(b'!'), _sharp=_ord(b'#'), _under=_ord(b'_'), _a=_ord(b'a'), _rcurl=_ord(b'}')):
    """
    Map a char to an integer

    >>> base92_ord(b'!')
    0
    >>> base92_ord(b'#')
    1
    >>> base92_ord(b'_')
    61
    >>> base92_ord(b'a')
    62
    >>> base92_ord(b'}')
    90
    >>> base92_ord(b' ')
    Traceback (most recent call last):
        ...
    ValueError: val is not a base92 character
    """
    num = _ord(val)
    if num == _excl:
        return 0
    elif _sharp <= num <= _under:
        return num - _sharp + 1
    elif _a <= num <= _rcurl:
        return num - _a + 62
    else:
        raise ValueError('val is not a base92 character')

 
def encode(bytstr):
    """
    Take a byte-string, and encode it in base 91

    >>> base92_encode(b"")
    '~'
    >>> base92_encode(b"\\x00")
    '!!'
    >>> base92_encode(b"\x01")
    '!B'
    >>> base92_encode(b"\xff")
    '|_'
    >>> base92_encode(b"aa")
    'D8*'
    >>> base92_encode(b"aaaaaaaaaaaaa")
    'D81RPya.)hgNA(%s'
    >>> base92_encode([16,32,48])
    "'_$,"
    """
    # always encode *something*, in case we need to avoid empty strings
    if not bytstr:
        return b'~'
    # make sure we have a bytstr
    if isinstance(bytstr, bytes):
        pass
    elif isinstance(bytstr, str):
        bytstr = bytstr.encode()
    else:
        # we'll assume it's a sequence of ints
        bytstr = b''.join(_chr(b) for b in bytstr)
    # prime the pump
    nbytes = len(bytstr)
    size = (nbytes * 8) % 13
    size = 2 * (nbytes * 8) // 13 + (0 if size == 0 else (1 if size < 7 else 2))
    resstr = bytearray(size)
    workspace = 0
    wssize = 0
    j = 0
    for byte in bytstr:
        workspace = workspace << 8 | _ord(byte)
        wssize += 8
        if wssize < 13:
            continue
        tmp = (workspace >> (wssize - 13)) & 8191
        resstr[j] = base92_chr(tmp // 91)
        j += 1
        resstr[j] = base92_chr(tmp % 91)
        j += 1
        wssize -= 13
    if wssize <= 0:
        pass
    elif wssize < 7:
        tmp = (workspace << (6 - wssize)) & 63
        resstr[j] = base92_chr(tmp)
        j += 1
    else:
        tmp = (workspace << (13 - wssize)) & 8191
        resstr[j] = base92_chr(tmp // 91)
        j += 1
        resstr[j] = base92_chr(tmp % 91)
        j += 1
    return bytes(resstr[:j])


def decode(bstr):
    """
    Take a base92 encoded string, convert it back to a byte-string

    >>> base92_decode(b"")
    ''
    >>> base92_decode(b"~")
    ''
    >>> base92_decode(b"!!")
    '\\x00'
    >>> base92_decode(b"!B")
    '\\x01'
    >>> base92_decode(b"|_")
    '\\xff'
    >>> base92_decode(b"D8*")
    'aa'
    >>> base92_decode(b"D81RPya.)hgNA(%s")
    'aaaaaaaaaaaaa'
    """
    if isinstance(bstr, str):
        bstr = bstr.encode()
    if bstr == b'~':
        return b''
    nbytes = len(bstr)
    size = ((nbytes // 2 * 13) + (nbytes % 2 * 6)) // 8
    resstr = bytearray(size)
    workspace = 0
    wssize = 0
    j = 0
    # we always have pairs of characters
    for i in range(nbytes // 2):
        workspace = (workspace << 13) | (base92_ord(bstr[2*i]) * 91 + base92_ord(bstr[2*i+1]))
        wssize += 13
        while wssize >= 8:
            resstr[j] = (workspace >> (wssize - 8)) & 255
            wssize -= 8
            j += 1
    # if we have an extra char, check for extras
    if nbytes % 2 == 1:
        workspace = (workspace << 6) | base92_ord(bstr[-1])
        wssize += 6
        while wssize >= 8:
            resstr[j] = (workspace >> (wssize - 8)) & 255
            wssize -= 8
            j += 1
    return bytes(resstr[:j])


base92_encode = b92encode = encode
base92_decode = b92decode = decode
