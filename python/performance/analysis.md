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

## Replace per-character lookup.

```
Encoding 1 chars: 391.38750999882177 ns
Encoding 6 chars: 1785.0584000007075 ns
Encoding 11 chars: 3243.667500000811 ns
Encoding 16 chars: 4662.363710003774 ns
Encoding 21 chars: 6034.675199998674 ns
Encoding 26 chars: 7610.088250003173 ns
Decoding to 1 chars: 440.61159000193584 ns
Decoding to 6 chars: 1907.6331300038873 ns
Decoding to 11 chars: 3329.9607200024184 ns
Decoding to 16 chars: 4695.564139992712 ns
Decoding to 21 chars: 6133.847889996105 ns
Decoding to 26 chars: 7678.189230000497 ns
```

## Bitwise Operations

```
Encoding 1 chars: 148.8203499957308 ns
Encoding 6 chars: 640.4161599948566 ns
Encoding 11 chars: 1130.1217399977759 ns
Encoding 16 chars: 1640.1831800067157 ns
Encoding 21 chars: 2166.5553500042734 ns
Encoding 26 chars: 2734.4605999951455 ns
Decoding to 1 chars: 239.81829000149446 ns
Decoding to 6 chars: 846.9768000031763 ns
Decoding to 11 chars: 1446.9558099972346 ns
Decoding to 16 chars: 2035.1283800027886 ns
Decoding to 21 chars: 2662.954659999741 ns
Decoding to 26 chars: 3276.007969998318 ns
```

## Preallocation

Weirdly enough, pre-allocating arrays worsens performance:

```
Encoding 1 chars: 209.56373999979405 ns
Encoding 6 chars: 596.0995699933846 ns
Encoding 11 chars: 995.7045499959349 ns
Encoding 16 chars: 1376.4785300008953 ns
Encoding 21 chars: 1760.7565700018313 ns
Encoding 26 chars: 2149.0727800028253 ns
Decoding to 1 chars: 310.41119000292383 ns
Decoding to 6 chars: 884.0166899972246 ns
Decoding to 11 chars: 1427.115259994025 ns
Decoding to 16 chars: 1977.6159599950918 ns
Decoding to 21 chars: 2544.8348600002646 ns
Decoding to 26 chars: 3080.5307300033746 ns
```

What about really long inputs? At that point Python arrays might need to be reallocated and then maybe there would be speed savings?

Previous:

```
Encoding 8192 chars: 1194766.1299927859 ns
Decoding to 8192 chars: 1983229.3599938569 ns
```

Preallocating:

```
Encoding 8192 chars: 1349843.5200017411 ns
Decoding to 8192 chars: 2168467.5500000594 ns
```

## C Module

Conversion to a C module speeds things up plenty:

```
Encoding 1 chars: 34.55212998233037 ns
Encoding 6 chars: 39.064980010152794 ns
Encoding 11 chars: 44.23369999130955 ns
Encoding 16 chars: 47.856160017545335 ns
Encoding 21 chars: 52.99060001561884 ns
Encoding 26 chars: 56.220330006908625 ns
Decoding to 1 chars: 25.94210996903712 ns
Decoding to 6 chars: 34.294940014660824 ns
Decoding to 11 chars: 38.33541002677521 ns
Decoding to 16 chars: 41.28248998313211 ns
Decoding to 21 chars: 44.64327001187485 ns
Decoding to 26 chars: 47.54287998366635 ns
```

As a comparison, encoding with base64 has comparable speed:

```
Base64 1 chars: 38.49617000014405 ns
Base64 6 chars: 42.65558999577479 ns
Base64 11 chars: 44.83564000111073 ns
Base64 16 chars: 48.365460006607464 ns
Base64 21 chars: 51.094649998049135 ns
Base64 26 chars: 54.77776000589074 ns
```

Interestingly, [base85 is just native Python](https://github.com/python/cpython/blob/3.13/Lib/base64.py#L293), so it is comparable to the Python-only base92:

```
Base85 1 chars: 519.7008499999356 ns
Base85 6 chars: 657.5137700019695 ns
Base85 11 chars: 772.7067399900989 ns
Base85 16 chars: 724.7526600076526 ns
Base85 21 chars: 1082.6245700081927 ns
Base85 26 chars: 1182.5178100116318 ns
```
