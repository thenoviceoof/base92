=====
base92
======

A little library for encoding byte-strings into strings easily
typeable on a standard US 101-key keyboard, with strictly better
information density than base64 or base85 encodings.

-----
USAGE
-----

Fire up your favorite python::

    >>> import base92
    >>> base92.decode(base92.encode('hello world'))
    'hello world'
    >>> base92.encode('\x61\xf2\x05\x99\x42')
    'DJ8gER!'

We use doctests, so running the tests is as easy as executing the
base92.py library file with your python.

----
MISC
----

This library has not been tested with python3.

There is more information available at
<https://github.com/thenoviceoof/base92>
