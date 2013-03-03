base92 = new Object

base92.encodeMapping =
        0: '!'
        1: '#'
        2: '$'
        3: '%'
        4: '&'
        5: '\''
        6: '('
        7: ')'
        8: '*'
        9: '+'
        10: ','
        11: '-'
        12: '.'
        13: '/'
        14: '0'
        15: '1'
        16: '2'
        17: '3'
        18: '4'
        19: '5'
        20: '6'
        21: '7'
        22: '8'
        23: '9'
        24: ':'
        25: ';'
        26: '<'
        27: '='
        28: '>'
        29: '?'
        30: '@'
        31: 'A'
        32: 'B'
        33: 'C'
        34: 'D'
        35: 'E'
        36: 'F'
        37: 'G'
        38: 'H'
        39: 'I'
        40: 'J'
        41: 'K'
        42: 'L'
        43: 'M'
        44: 'N'
        45: 'O'
        46: 'P'
        47: 'Q'
        48: 'R'
        49: 'S'
        50: 'T'
        51: 'U'
        52: 'V'
        53: 'W'
        54: 'X'
        55: 'Y'
        56: 'Z'
        57: '['
        58: '\\'
        59: ']'
        60: '^'
        61: '_'
        62: 'a'
        63: 'b'
        64: 'c'
        65: 'd'
        66: 'e'
        67: 'f'
        68: 'g'
        69: 'h'
        70: 'i'
        71: 'j'
        72: 'k'
        73: 'l'
        74: 'm'
        75: 'n'
        76: 'o'
        77: 'p'
        78: 'q'
        79: 'r'
        80: 's'
        81: 't'
        82: 'u'
        83: 'v'
        84: 'w'
        85: 'x'
        86: 'y'
        87: 'z'
        88: '{'
        89: '|'
        90: '}'


base92.decodeMapping =
        '!': 0
        '#': 1
        '$': 2
        '%': 3
        '&': 4
        '\'': 5
        '(': 6
        ')': 7
        '*': 8
        '+': 9
        ',': 10
        '-': 11
        '.': 12
        '/': 13
        '0': 14
        '1': 15
        '2': 16
        '3': 17
        '4': 18
        '5': 19
        '6': 20
        '7': 21
        '8': 22
        '9': 23
        ':': 24
        ';': 25
        '<': 26
        '=': 27
        '>': 28
        '?': 29
        '@': 30
        'A': 31
        'B': 32
        'C': 33
        'D': 34
        'E': 35
        'F': 36
        'G': 37
        'H': 38
        'I': 39
        'J': 40
        'K': 41
        'L': 42
        'M': 43
        'N': 44
        'O': 45
        'P': 46
        'Q': 47
        'R': 48
        'S': 49
        'T': 50
        'U': 51
        'V': 52
        'W': 53
        'X': 54
        'Y': 55
        'Z': 56
        '[': 57
        '\\': 58
        ']': 59
        '^': 60
        '_': 61
        'a': 62
        'b': 63
        'c': 64
        'd': 65
        'e': 66
        'f': 67
        'g': 68
        'h': 69
        'i': 70
        'j': 71
        'k': 72
        'l': 73
        'm': 74
        'n': 75
        'o': 76
        'p': 77
        'q': 78
        'r': 79
        's': 80
        't': 81
        'u': 82
        'v': 83
        'w': 84
        'x': 85
        'y': 86
        'z': 87
        '{': 88
        '|': 89
        '}': 90

base92.encode = (bytes) ->
        if bytes.length == 0
                return '~'
        res = ''
        # we do bit twiddling here, b/c arrays seem like a heavy solution
        # with 53 bits to fit 13+8 bits (off the cuff max) not a problem
        workspace = 0 # where to keep the bits
        wssize = 0 # how many bits are there
        for b in bytes
                workspace = workspace * 256 + b
                wssize += 8
                if wssize >= 13
                        tmp = (workspace / Math.pow(2,wssize-13)) & 8191
                        res += base92.encodeMapping[Math.floor(tmp/91)]
                        res += base92.encodeMapping[Math.floor(tmp%91)]
                        # we'll want to reduce the size, b/c fp prec
                        wssize -= 13
                        workspace = workspace & (Math.pow(2, wssize) - 1)
        if 0 < wssize and wssize < 7
                tmp = workspace * Math.pow(2, 6 - wssize) & 63
                res += base92.encodeMapping[tmp]
        else if 7 <= wssize
                tmp = workspace * Math.pow(2, 13 - wssize) & 8191
                res += base92.encodeMapping[Math.floor(tmp/91)]
                res += base92.encodeMapping[Math.floor(tmp%91)]
        return res

base92.decode = (str) ->
        if str.length == 0 or str == '~'
                return [0]
        if str.length < 2
                return undefined
        # handle pairs
        res = []
        workspace = 0
        wssize = 0
        for i in [0..str.length - 1] by 2
                b1 = base92.decodeMapping[str[i]]
                b2 = base92.decodeMapping[str[i+1]]
                workspace = workspace * 8192 + (91 * b1 + b2)
                wssize += 13
                while wssize >= 8
                        tmp = workspace / Math.pow(2, wssize - 8)
                        res.push Math.round(tmp) & 255
                        wssize -= 8
                        # reduce the upper bits, for fp precision
                        workspace = workspace & (Math.pow(2, wssize) - 1)
        # handle single chars
        if str.length % 2 == 1
                b = base92.decodeMapping[str[str.length - 1]]
                workspace = workspace / 64 + b
                wssize += 6
                while wssize >= 8
                        tmp = workspace / Math.pow(2, wssize - 8)
                        res.push Math.round(tmp) & 255
                        wssize -= 8
        return res

# make me a module
define base92
