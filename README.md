NOTE: this is NOT suitable for general consumption yet, and may never
be. There are some problems detailed below, and as such you should use
base64 or base85 (in case you somehow stumbled across this without
knowing about those)

base92
================================================================================
A little python library for encoding byte-strings into strings easily
typeable on a standard US 101-key keyboard.


USAGE
--------------------------------------------------------------------------------
Fire up your favorite python:

    import base92
    base92.decode(base92.encode('hello world'))
    base92.b92encode('goodbye')


DESIGN DECISIONS
--------------------------------------------------------------------------------
We are going to try and be clever, and leave out some characters from
the general encoding scheme:

    ~, `, "

The ` and " are just too similar to a normal quote for comfort.

However, we'll use ~ for a special denotation: there are 94 printable
ascii characters, so we end up with 91 characters, or 6.5 bits per
character. Once we include the ~, then we have 92 characters: hence,
base92.

(honestly, base91 was just too ugly a name to deal with)

Note: the use of ~ does make the length of the output non-monotonic
with the length of the input, unlike base64 and base85. This is
undesirable (if only from an elegance standpoint), and if it irks me
sufficiently I'll try to figure out how to fix it.

NOTE: base64 and base85 are much more elegant, cleanly
mapping a small integer of bytes onto another small integer of
bytes. base92 maps 13 bytes to 16 characters, which is better than
base85's 4 to 5, but is fairly inelegant.


BENCHMARKS
--------------------------------------------------------------------------------
On average, characters saved:
  For string lengths 1-32:

    base64-base92 | base85-base92
    -----------------------------
    1.677           -0.645

  For string lengths 1-128:

    base64-base92 | base85-base92
    -----------------------------
    6.590           0.291

Over the short strings, base85 wins because it is better designed:
base92 starts to win over longer strings only because of its greater
interior bit density.
