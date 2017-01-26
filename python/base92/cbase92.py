# THE BEERWARE LICENSE (Revision 42):
# <thenoviceoof> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer in return
# - Nathan Hwang (thenoviceoof)

'''
base92: a library for encoding byte strings

>>> x = encode('hello world')
>>> x
'Fc_$aOTdKnsM*k'
>>> decode(x)
'hello world'

>>> y = encode('^\xb6;\xbb\xe0\x1e\xee\xd0\x93\xcb"\xbb\x8fZ\xcd\xc3')
>>> y
"C=i.w6'IvB/viUpRAwco"
>>> decode(y)
'^\\xb6;\\xbb\\xe0\\x1e\\xee\\xd0\\x93\\xcb"\\xbb\\x8fZ\\xcd\\xc3'

this is a regression test
>>> decode(encode('aoeuaoeuaoeu'))
'aoeuaoeuaoeu'
'''

__version__ = (1, 0, 3)

__all__ = [
    'encode',
    'decode',
    'b92encode',
    'b92decode',
    'base92encode',
    'base92decode',
]

from base92_extension import encode, decode

base92_encode = b92encode = encode
base92_decode = b92decode = decode


def test():
    import doctest
    doctest.testmod()

    ## more correctness tests
    import hashlib
    import random
    def gen_bytes(s):
        return hashlib.sha512(s).digest()[:random.randint(1,64)]
    for _ in range(10000):
        s = gen_bytes(bytes(random.random()))
        assert s == decode(encode(s)), 'decode(encode({!r})) = decode({!r}) = {!r}'.format(s, encode(s), decode(encode(s)))
    print('correctness spot check passed')

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

    
if __name__ == "__main__":
    test()
