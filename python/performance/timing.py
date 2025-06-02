import timeit

N = 100000
print("Running encode/decode with {} iterations over 24 characters".format(N))

# Add the parent directory to path so we can import base92.
ENCODE_SETUP = """
import hashlib
import random
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base92 import base92
data = hashlib.sha512(str(random.random()).encode('utf8')).digest()[: {}]
"""
ENCODE_RUNNER = "base92.encode(data)"
for i in range(1, 27, 5):
    time = timeit.timeit(ENCODE_RUNNER, ENCODE_SETUP.format(i), number=N) / N
    print("Encoding {} chars: {} ns".format(i, time * 1e9))

DECODE_SETUP = """
import hashlib
import random
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base92 import base92
data = hashlib.sha512(str(random.random()).encode('utf8')).digest()[: {}]
encoded = base92.encode(data)
"""
DECODE_RUNNER = "base92.decode(encoded)"
for i in range(1, 27, 5):
    time = timeit.timeit(DECODE_RUNNER, DECODE_SETUP.format(i), number=N) / N
    print("Decoding to {} chars: {} ns".format(i, time * 1e9))
