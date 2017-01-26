base92
================================================================================
A little library for encoding byte-strings into strings easily
typeable on a standard US 101-key keyboard.


INSTALLATION
--------------------------------------------------------------------------------
The C library is built with the GNU development tools
(automake/autoconf), and can be built in the usual way with a `make
install`.

The python library is available through pypi
(http://pypi.python.org/pypi/base92/) with `pip install base92`, or
with `python setup.py install`.


USAGE
--------------------------------------------------------------------------------

### C ###

To build as a shared library in $PREFIX.

    mkdir -p $PREFIX/include/ $PREFIX/lib/
    gcc -shared -Wl,-soname,libbase92 -o $PREFIX/lib/libbase92.so -fPIC -Ic/src c/src/base92.c
    cp -a c/src/base92.h $PREFIX/include/

Use:

    #include <base92.h>
    ...
    strcmp(base92encode("hello world", 11), "Fc_$aOTdKnsM*k") == 0;
    base92decode("Fc_$aOTdKnsM*k", &length);
    length == 11;
    ...

### Python ###

To build:

    cd python
    python setup.py build_ext --inplace
    python setup.py install

Fire up your favorite python:

    >>> import base92
    >>> base92.decode(base92.encode('hello world'))
    'hello world'
    >>> base92.b92encode('\x61\xf2\x05\x99\x42')
    'DJ8gER!'


DESIGN DECISIONS
--------------------------------------------------------------------------------
We are going to try and be clever, and leave out some printable ASCII
characters from the general encoding scheme:

    ~, `, "

The ` and " are just too similar to a normal quote ' for comfort when
typing out encoded strings. Hopefully you're using a good font when
differentiating between l/1 and 0/O.

However, we'll use ~ for a special denotation (an empty string).
There are 94 printable ascii characters, so we end up with 91
characters, or 6.5 bits per character. Once we include the ~, then we
have 92 characters: hence, base92.

(and honestly, base91 was just too ugly a name to deal with)

Once we have 6.5 bits per characters, then we can take 13 bits at a
time and produce two output characters with them, using a division and
modulo scheme similar to base85. This might mean than base92 encoding
is more resistant to corruption, because any corruption is more
localized (one bit change affects only 2-3 bytes, not 4).

Note: the use of ~ as an empty string denoter might be needed in some
cases that expect some output: however, passing an empty string to
decode will not cause it to barf, so it's not a requirement to use ~.

Sidenote: previously base92 produced output that grew in length that
was nonmonotonic with the length of the input. This is no longer the case.

Another sidenote: base64 and base85 are much more elegant, cleanly
mapping a small integer of bytes onto another small integer of
bytes. base92 maps 13 bytes to 16 characters, which is better than
base85's 4 to 5 from a size perspective, but is fairly inelegant.

We also follow base85's convention of using the high divisor product
as the first bytes.


BENCHMARKS
--------------------------------------------------------------------------------
On average, characters saved:

  For string lengths 1-32:

    base64-base92 | base85-base92
    -----------------------------
    2.548           0.226

  For string lengths 1-128:

    base64-base92 | base85-base92
    -----------------------------
    7.441           1.142

Here, we see that base92 strictly wins in size over base64 and base85,
as is expected with a higher bit density encoding.

There are no speed benchmarks, because this is a pure python
implementation and I wouldn't want to benchmark anything that's not a
native C library.


THANKS
--------------------------------------------------------------------------------
 - tly1980: Filed issue #3
 - l31g: helped with resolving issue #3
 - seanyeh: helped with resolving issue #3


LICENSE
--------------------------------------------------------------------------------
THE BEERWARE LICENSE (Revision 42):

@thenoviceoof wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you
think this stuff is worth it, you can buy me a beer in return

- Nathan Hwang (thenoviceoof)
