"""
Import routines from base92.cbase92 or base92.base92 for manipulating base92 encoded strings.

Example:

>>> from base92 import encode, decode, b92encode, b92decode
>>> x = encode('hello world')
>>> x
'Fc_$aOTdKnsM*k'
>>> decode(x)
'hello world'
"""

from . import base92

try:
    from . import cbase92
    preferred_base92 = cbase92
except (ImportError, OSError) as e:
    print('Falling back to base92 python backend due to: {}'.format(e))
    preferred_base92 = base92
    cbase92 = None

encode = b92encode = preferred_base92.encode
decode = b92decode = preferred_base92.decode
__version__ = base92.__version__
