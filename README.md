base92
================================================================================
A little python library for encoding byte-strings into strings easily
typeable on a standard US 101-key keyboard.


USAGE
--------------------------------------------------------------------------------
Fire up your favorite python:

    >>> import base92
    >>> base92.decode(base92.encode('hello world'))
    'hello world'
    >>> base92.b92encode('\x61\xf2\x05\x99\x42')
    'DJ8gER!'


DESIGN DECISIONS
--------------------------------------------------------------------------------
We are going to try and be clever, and leave out some characters from
the general encoding scheme:

    ~, `, "

The ` and " are just too similar to a normal quote ' for comfort.

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
