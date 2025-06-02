"""
Import routines from base92.base92 for manipulating base92 encoded strings.

Example:

>>> from base92 import encode, decode, b92encode, b92decode
>>> x = encode('hello world')
>>> x
'Fc_$aOTdKnsM*k'
>>> decode(x)
'hello world'
"""

__version__ = (2, 0, 0)

try:
    from ._base92compiled import base92_encode, base92_decode
except ImportError:
    from ._base92python import base92_encode, base92_decode

# Define aliases.
encode = base92_encode
b92encode = base92_encode

decode = base92_decode
b92decode = base92_decode
