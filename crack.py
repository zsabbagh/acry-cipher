"""
    Cipher
"""
import sys
import os
import re
import time # .sleep(), .time(), .time_ns()

"""
    Ideas:
    - Statistical analysis
"""

ALPHA = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#'
DEFAULT = '1.data'
MOST_COMMON = 'ETAOINSHRDLUCWMFYGPBVKXJQZ'

def count(d, k):
    if k not in d:
        d[k] = 1
    else:
        d[k] += 1

def main():
    args = sys.argv[1:]
    path = None

    for i in range(0, len(args)):
        f = args[i]
        if f[0] != '-':
            path = f

    if path is None:
        path = DEFAULT

    file = open(path, 'r').read().rstrip()
    file = ''.join(file.split('\n'))

    dct = {}
    for c in file:
        count(dct, c)

    ls = []
    for c in dct:
        ls.append((c, dct[c]))

    ls = sorted(ls, key=lambda x : x[1])
    for (c, v) in ls:
        print(c + ": " + str(v))

if __name__ == "__main__":
    main()
