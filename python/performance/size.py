# Used to derive the size advantage of base92 over base64/base85 which
# is used in the README.
import base64
import base85
from pprint import pprint
sd = [(len(base64.b64encode('a'*i)),
       len(base85.b85encode('a'*i)),
       len(encode('a'*i)))
      for i in range(1,128)]
pprint(sd)
print(sum(a-c for a,b,c in sd)/float(len(sd)))
print(sum(b-c for a,b,c in sd)/float(len(sd)))
