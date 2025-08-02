# Used to derive the size advantage of base92 over base64/base85,
# described in docs/encoding.md.
import base64
from pprint import pprint
import base92

sd = [
    (
        len(base64.b64encode(b"a" * i)),
        len(base64.a85encode(b"a" * i)),
        len(base92.b92encode(b"a" * i)),
    )
    for i in range(1, 128)
]
pprint(sd)
print(sum(a - c for a, b, c in sd) / float(len(sd)))
print(sum(b - c for a, b, c in sd) / float(len(sd)))
