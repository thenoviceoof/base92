'''
Import routines from base92.cbase92 or base92.base92 for manipulating base92 encoded strings.

Example:

>>> from base92 import encode, decode, b92encode, b92decode
>>> x = encode('hello world')
>>> x
'Fc_$aOTdKnsM*k'
>>> decode(x)
'hello world'
'''
try:
    from .cbase92 import encode, decode, b92encode, b92decode, __version__
except (ImportError, OSError) as e:
    print('Falling back to base92 python backend due to: {}'.format(e))
    from .base92 import encode, decode, b92encode, b92decode, __version__
