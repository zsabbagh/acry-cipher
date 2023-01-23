"""
    Cipher cracker
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

def stats(dct, repl):
    """
        Statistical approach
    """
    pass

def modulo():
    """
        Modular
    """

def perm():
    """
        Permutator
    """

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

    chars = {}
    chars2 = {}
    for i in range(0, len(file)):
        count(chars, file[i])
        if i > 0:
            count(chars2, file[i-1:i+1])

    ls = []
    for c in chars:
        ls.append((c, chars[c]))

    ls = sorted(ls, key=lambda x : x[1])
    for (c, v) in ls:
        print(c + ": " + str(v))

if __name__ == "__main__":
    main()
