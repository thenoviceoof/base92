import timeit

N = 100000
print("Running encode/decode with {} iterations over 24 characters".format(N))

ENCODE_SETUP = """
import hashlib
import random
from base92 import base92
data = b'a' * {}
"""
ENCODE_RUNNER = "base92.encode(data)"
for i in range(1, 27, 5):
    time = timeit.timeit(ENCODE_RUNNER, ENCODE_SETUP.format(i), number=N) / N
    print("Encoding {} chars: {} ns".format(i, time * 1e9))

DECODE_SETUP = """
import hashlib
import random
from base92 import base92
data = b'a' * {}
encoded = base92.encode(data)
"""
DECODE_RUNNER = "base92.decode(encoded)"
for i in range(1, 27, 5):
    time = timeit.timeit(DECODE_RUNNER, DECODE_SETUP.format(i), number=N) / N
    print("Decoding to {} chars: {} ns".format(i, time * 1e9))
