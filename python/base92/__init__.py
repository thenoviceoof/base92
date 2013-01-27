'''
Import routines from base92.base92 for manipulating base92 encoded strings.

Example:

>>> from base92 import encode, decode, b92encode, b92decode
>>> x = encode('hello world')
>>> x
'Fc_$aOTdKnsM*k'
>>> decode(x)
'hello world'
'''

from base92 import encode, decode, b92encode, b92decode, __version__
