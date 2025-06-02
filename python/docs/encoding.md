# base92 Encoding details

## Prior Art

- [2005 Patent](https://patents.google.com/patent/US20030152220A1/en) (not related, except that it's using the same basic ideas).
- [A 2016 Hacker News comment](https://news.ycombinator.com/item?id=13052787) details a different base92 encoding.

## Design Decisions

We are going to try and be clever, and leave out some printable ASCII
characters from the general encoding scheme:

```
~, `, "
```

The ` and " are just too similar to a normal quote ' for comfort when
typing out encoded strings. Hopefully you're using a good font when
differentiating between l/1 and 0/O.

However, we'll use ~ for a special denotation (an empty string). There
are 94 printable ascii characters, so we end up with 91 characters, or
6.5 bits per character. Once we include the ~, then we have 92
characters: hence, base92.

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
was nonmonotonic with the length of the input. This is no longer the
case.

Another sidenote: base64 and base85 are much more elegant, cleanly
mapping a small integer of bytes onto another small integer of
bytes. base92 maps 13 bytes to 16 characters, which is better than
base85's 4 to 5 from a size perspective, but is fairly inelegant.

We also follow base85's convention of using the high divisor product
as the first bytes.

## Size savings

On average, characters saved for string lengths 1-32:

```
base64-base92 | base85-base92
-----------------------------
2.548           0.226
```

For string lengths 1-128:

```
base64-base92 | base85-base92
-----------------------------
7.441           1.142
```

Here, we see that base92 strictly wins in size over base64 and base85,
as is expected with a higher bit density encoding.

That said, encoding a 128 bytestring with base85 uses 159 bytes, while
base92 uses... 157 bytes. 2 bytes might not be worth it to add another
dependency, but maybe your use case is extremely sensitive to lengths,
and requires ASCII-compatible language users to type in encodings.
