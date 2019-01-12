import time
import random

from . import base92, cbase92


def gen_bytes(maxlen=255):
    return bytes(bytearray(random.getrandbits(8) for _ in range(random.randint(0, 255))))


def cross_validate(modules, to_encode, expected_encoded=None):
    encoded = {m: m.encode(to_encode) for m in modules}
    if expected_encoded is not None:
        encoded['expected'] = expected_encoded
    assert len(set(encoded.values())) == 1, 'different encodings of {!r}: {}'.format(to_encode, encoded)
    decoded = {(m_enc, m_dec): m_dec.decode(data) for m_enc, data in encoded.items() for m_dec in modules}
    decoded['expected'] = to_encode
    assert len(set(decoded.values())) == 1, 'different decodings of {!r}: {}\nencodings: {}'.format(to_encode, decoded, encoded)


def run(modules=(base92, cbase92), random_count=10000, silent=False):
    modules = list({m for m in modules if m})

    if not silent:
        print('testing and cross validating encoders and decoders from modules {}'.format(modules))

    for s, e in [(b'', b'~'), (b'b', b'DL'), (b'hello world', b'Fc_$aOTdKnsM*k'), (b'\x93', b'Ub')]:
        cross_validate(modules, s, e)
    
    if not silent:
        print('selected regression tests passed\ngenerating {} random byte strings'.format(random_count))

    # more correctness tests

    random_bytes = [gen_bytes() for _ in range(random_count)]
    for s in random_bytes:
        cross_validate(modules, s)

    if not silent:
        print('{} randomized X == decode(encode(X)) tests passed'.format(random_count))

    for m in modules:
        enc = 0.0
        dec = 0.0
        for s in random_bytes:
            start_enc = time.time()
            x = m.encode(s)
            stop_enc = time.time()
            enc += stop_enc - start_enc
            m.decode(x)
            dec += time.time() - stop_enc
        print('performance of module {} on the {} random byte strings'.format(m, random_count))
        print('- encoding: {}s'.format(enc))
        print('- decoding: {}s'.format(dec))

    # size tests
    # import base64
    # import base85
    # from pprint import pprint
    # sd = [(len(base64.b64encode('a'*i)),
    #        len(base85.b85encode('a'*i)),
    #        len(encode('a'*i)))
    #       for i in range(1,128)]
    # pprint(sd)
    # print sum(a-c for a,b,c in sd)/float(len(sd))
    # print sum(b-c for a,b,c in sd)/float(len(sd))


if __name__ == '__main__':
    run()
