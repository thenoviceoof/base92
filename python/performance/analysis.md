# Performance Analysis

## Version 1.0.3

This performance is measured against

- The pure Python implementation...
- After being ported to Python 3...
- ... But before being uploaded anywhere.
- As measured by the timing.py script in the same directory.

```
Running encode/decode with 100000 iterations over 24 characters
Encoding 1 chars: 454.5139299989387 ns
Encoding 6 chars: 1981.9814399988898 ns
Encoding 11 chars: 3548.973679999108 ns
Encoding 16 chars: 5091.094909998901 ns
Encoding 21 chars: 6858.2971500018175 ns
Encoding 26 chars: 8199.840649999715 ns
Decoding to 1 chars: 583.676920000471 ns
Decoding to 6 chars: 2208.5008800013384 ns
Decoding to 11 chars: 4019.167569999809 ns
Decoding to 16 chars: 5673.087770001075 ns
Decoding to 21 chars: 7338.8345500006835 ns
Decoding to 26 chars: 9177.229749998332 ns
```
