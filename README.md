base91
================================================================================
A little python library for encoding byte-strings into strings easily
typeable on a standard US 101-key keyboard.

DESIGN DECISIONS
--------------------------------------------------------------------------------
We are going to try and be clever, and leave out:
   ~, `, "

The ` and " are just too close to ' for comfort

However, we'll use ~ for denoting an end

There are 94 printable ascii characters, so we end up with 91
characters, or 6.5 bits per character
