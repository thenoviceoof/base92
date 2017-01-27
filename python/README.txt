======
base92
======

A little library for encoding byte-strings into strings easily
typeable on a standard US 101-key keyboard, with strictly better
information density than base64 or base85 encodings.

It is python3 compatible and has a C backend.

--------
BUILDING
--------

Compile the C extension and install.

    python setup.py build_ext --inplace  # creates base92/base92_extension.so
    python setup.py install

-----
USAGE
-----

Fire up your favorite python::

    >>> import base92
    >>> base92.decode(base92.encode('hello world'))
    'hello world'
    >>> base92.encode('\x61\xf2\x05\x99\x42')
    'DJ8gER!'
    
    >>> import base92.test
    >>> base92.test.run()
    testing and cross validating encoders and decoders from modules [<module 'base92.cbase92' from 'base92/cbase92.pyc'>, <module 'base92.base92' from 'base92/base92.py'>]
    selected regression tests passed
    generating 10000 random byte strings
    10000 randomized X == decode(encode(X)) tests passed
    performance of module <module 'base92.cbase92' from 'base92/cbase92.pyc'> on the 10000 random byte strings
    - encoding: 0.00835490226746s
    - decoding: 0.00846481323242s
    performance of module <module 'base92.base92' from 'base92/base92.py'> on the 10000 random byte strings
    - encoding: 1.75639009476s
    - decoding: 1.28861784935s

If the C backend is not available, the python backend will be used:

    rm -f base92/base92_extension.so

    >>> import base92
    Falling back to base92 python backend due to: No module named base92_extension

We use doctests, so running the tests is as easy as executing the
base92.py library file with your python.

----
MISC
----

This library has a C extension as a backend and falls back to python if the backend isn't available.

There is more information available at
<https://github.com/thenoviceoof/base92>
