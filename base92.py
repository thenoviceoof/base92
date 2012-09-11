# THE BEERWARE LICENSE (Revision 42):
# <thenoviceoof> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer in return
# - Nathan Hwang (thenoviceoof)

'''
base92: a library for encoding byte strings

>>> x = encode('hello world')
>>> x
'Fc_$aOTdKnsM#+'
>>> decode(x)
'hello world'

>>> y = encode('^\xb6;\xbb\xe0\x1e\xee\xd0\x93\xcb"\xbb\x8fZ\xcd\xc3')
>>> y
"C=i.w6'IvB/viUpRAw25"
>>> decode(y)
'^\\xb6;\\xbb\\xe0\\x1e\\xee\\xd0\\x93\\xcb"\\xbb\\x8fZ\\xcd\\xc3'
'''

import math

__version__ = (0, 0, 1)

def base92_chr(val):
    '''
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
    '''
    if val < 0 or val >= 91:
        raise ValueError('val must be in [0, 91)')
    if val == 0:
        return '!'
    elif val <= 61:
        return chr(ord('#') + val - 1)
    else:
        return chr(ord('a') + val - 62)

def base92_ord(val):
    '''
    Map a char to an integer

    >>> base92_ord('!')
    0
    >>> base92_ord('#')
    1
    >>> base92_ord('_')
    61
    >>> base92_ord('a')
    62
    >>> base92_ord('}')
    90
    >>> base92_ord(' ')
    Traceback (most recent call last):
        ...
    ValueError: val is not a base92 character
    '''
    num = ord(val)
    if val == '!':
        return 0
    elif ord('#') <= num and num <= ord('_'):
        return num - ord('#') + 1
    elif ord('a') <= num and num <= ord('}'):
        return num - ord('a') + 62
    else:
        raise ValueError('val is not a base92 character')

def base92_encode(bytstr):
    '''
    Take a byte-string, and encode it in base 91

    >>> base92_encode("")
    '~'
    >>> base92_encode("\\x00")
    '!!'
    >>> base92_encode("\x01")
    '!B'
    >>> base92_encode("\xff")
    '|_'
    >>> base92_encode("aa")
    'D8-9~'
    >>> base92_encode("hello world")
    'Fc_$aOTdKnsM#+'
    >>> base92_encode("aaaaaaaaaaaaa")
    'D81RPya.)hgNA(%s'
    '''
    # always encode *something*, in case we need to avoid empty strings
    if not bytstr:
        return '~'
    # check if we need a lop char at the end
    lop = False
    if (8 * (len(bytstr) + 1) <
        13 * min(x for x in range(len(bytstr)+1) if 13*x >= 8*len(bytstr))):
        lop = True
    # prime the pump
    bitstr = '{:08b}'.format(ord(bytstr[0]))
    bytstr = bytstr[1:]
    resstr = ''
    while len(bytstr):
        while len(bitstr) < 13 and bytstr:
            bitstr += '{:08b}'.format(ord(bytstr[0]))
            bytstr = bytstr[1:]
        i = int(bitstr[:13], 2)
        resstr += base92_chr(i / 91)
        resstr += base92_chr(i % 91)
        bitstr = bitstr[13:]
    if bitstr:
        bitstr += '0' * (13 - len(bitstr))
        i = int(bitstr, 2)
        resstr += base92_chr(i / 91)
        resstr += base92_chr(i % 91)
    if lop:
        resstr += '~'
    return resstr

def base92_decode(bstr):
    '''
    Take a base92 encoded string, convert it back to a byte-string

    >>> base92_decode("")
    ''
    >>> base92_decode("~")
    ''
    >>> base92_decode("!!")
    '\\x00'
    >>> base92_decode("!B")
    '\\x01'
    >>> base92_decode("|_")
    '\\xff'
    >>> base92_decode("D8-9~")
    'aa'
    >>> base92_decode('Fc_$aOTdKnsM#+')
    'hello world'
    >>> base92_decode("D81RPya.)hgNA(%s")
    'aaaaaaaaaaaaa'
    '''
    bitstr = ''
    resstr = ''
    # we always have pairs of characters
    for i in range(len(bstr)/2):
        x = base92_ord(bstr[2*i])*91 + base92_ord(bstr[2*i+1])
        bitstr += "{:013b}".format(x)
        while 8 <= len(bitstr):
            resstr += chr(int(bitstr[0:8], 2))
            bitstr = bitstr[8:]
    # check if we have a lop char
    if bstr and bstr[-1] == '~':
        resstr = resstr[:-1]
    return resstr

encode = base92_encode
decode = base92_decode

if __name__ == "__main__":
    import doctest
    doctest.testmod()
