======
base92
======

A little library for encoding byte-strings into strings easily
typeable on a standard US 101-key keyboard, with strictly better
information density than base64 or base85 encodings.

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

Test the backends in ipython:

    In [1]: import base92.base92

    In [2]: base92.base92.test()
    correctness spot check passed

    In [3]: %timeit base92.base92.test()
    correctness spot check passed
    # ...
    correctness spot check passed
    1 loop, best of 3: 1.36 s per loop

    In [4]: import base92.cbase92

    In [5]: base92.cbase92.test()
    correctness spot check passed

    In [6]: %timeit base92.cbase92.test()
    correctness spot check passed
    # ...
    correctness spot check passed
    10 loops, best of 3: 53.3 ms per loop

    In [7]: import base92

    In [8]: base92.encode is base92.cbase92.encode
    OUT[8]: True

If the C backend is not available, the python backend will be used:

    rm -f base92/base92_extension.so

    In [1]: import base92
    Falling back to base92 python backend due to: No module named base92_extension

    In [2]: import base92.base92

    In [3]: base92.encode is base92.base92.encode
    Out[3]: True

We use doctests, so running the tests is as easy as executing the
base92.py library file with your python.

----
MISC
----

This library has a C extension as a backend and falls back to python if the backend isn't available.

This library has not been tested with python3.

There is more information available at
<https://github.com/thenoviceoof/base92>
