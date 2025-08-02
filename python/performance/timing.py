import timeit

N = 100000
print("Running encode/decode with {} iterations over 24 characters".format(N))

ENCODE_SETUP = """
import hashlib
import random
import base92
data = b'a' * {}
"""
ENCODE_RUNNER = "base92.encode(data)"
for i in range(1, 27, 5):
    time = timeit.timeit(ENCODE_RUNNER, ENCODE_SETUP.format(i), number=N) / N
    print("Encoding {} chars: {} ns".format(i, time * 1e9))

DECODE_SETUP = """
import hashlib
import random
import base92
data = b'a' * {}
encoded = base92.encode(data)
"""
DECODE_RUNNER = "base92.decode(encoded)"
for i in range(1, 27, 5):
    time = timeit.timeit(DECODE_RUNNER, DECODE_SETUP.format(i), number=N) / N
    print("Decoding to {} chars: {} ns".format(i, time * 1e9))

# Compare some longer inputs.
time = timeit.timeit(ENCODE_RUNNER, ENCODE_SETUP.format(16384), number=100) / 100
print("Encoding {} chars: {} ns".format(8192, time * 1e9))
time = timeit.timeit(DECODE_RUNNER, DECODE_SETUP.format(16384), number=100) / 100
print("Decoding to {} chars: {} ns".format(8192, time * 1e9))

# Compare against base64/base85.

B64_ENCODE_SETUP = """
import hashlib
import random
import base64
data = b'a' * {}
"""
B64_ENCODE_RUNNER = "base64.b64encode(data)"
for i in range(1, 27, 5):
    time = timeit.timeit(B64_ENCODE_RUNNER, B64_ENCODE_SETUP.format(i), number=N) / N
    print("Base64 {} chars: {} ns".format(i, time * 1e9))

B85_ENCODE_SETUP = """
import hashlib
import random
import base64
data = b'a' * {}
"""
B85_ENCODE_RUNNER = "base64.b85encode(data)"
for i in range(1, 27, 5):
    time = timeit.timeit(B85_ENCODE_RUNNER, B85_ENCODE_SETUP.format(i), number=N) / N
    print("Base85 {} chars: {} ns".format(i, time * 1e9))
