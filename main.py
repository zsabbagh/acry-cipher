"""
    Cipher cracker
"""
import sys
import os
import re
import time # .sleep(), .time(), .time_ns()
import argparse

"""
    Ideas:
    - Statistical analysis
"""

ALPHA = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#'
ALPHAS = [ALPHA, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_#0123456789', '_#0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ']
DEFAULT = '1.data'
DEFAULT_FREQUENCY = 'freq.data'
MOST_COMMON = 'ETAOINSHRDLUCWMFYGPBVKXJQZ'

def stats(count, freq, demo_text, bound=0):
    """
        Statistical approach
    """
    bounds = [freq]
    if type(freq) is not list:
        freq = list(freq)
    for i in range(0, len(count)):
        if count[i] not in freq:
            freq.append(count[i])
        else:
            print(count[i] + ' -> ' + freq[i])
    new = []
    for c in demo_text:
        new.append(freq[count.index(c)])
    print(''.join(new))

def modulo(text):
    """
        Modular
    """
    for alpha in ALPHAS:
        print("\n\n----- NEW ALPHA : " + alpha + " -----")
        for inc in range(0, len(alpha)):
            print("inc = " + str(inc))
            new = []
            for i in range(0, len(text)):
                new.append(alpha[(alpha.index(text[i])+inc) % len(alpha)])
            print(''.join(new))

def perm():
    """
        Permutator
    """

def counter(d, k):
    if k not in d:
        d[k] = 1
    else:
        d[k] += 1

def get_freq(text, bi=False):
    """
        Get characters in a list ordered by frequency
    """
    chars = {}
    for i in range(0, len(text)):
        if bi and i > 0:
            counter(chars, text[i-1:i+1])
        else:
            counter(chars, text[i])
    ls = []
    for c in chars:
        ls.append([c, chars[c]])
    ls = sorted(ls, key=lambda x : x[1], reverse=True)
    ls = [x[0] for x in ls]
    return ls

def main():
    args = sys.argv[1:]
    freq_path = DEFAULT_FREQUENCY
    
    parser = argparse.ArgumentParser(
                    prog = 'crack',
                    description = 'Crack the ciphers of ACry course',
                    epilog = 'Cracking the cipher.')
    parser.add_argument('path', help='the cipher to crack')      # option that takes a value
    
    parser.add_argument('-m', '--modulo', help='enable modulo', action='store_true')
    parser.add_argument('-s', '--stats', help='enable modulo', action='store_true')
    parser.add_argument('-f', '--freq', nargs='?',
                        default=DEFAULT_FREQUENCY, 
                        help='frequency file of characters in order of most common', 
                        type=str)  # on/off flag
    parser.add_argument('-l', '--length', help='demo text length', default=100, type=int)
    args = parser.parse_args()

    if args.freq:
        freq_path = args.freq

    file = ''.join(open(args.path, 'r').read().rstrip().split('\n'))
    freq = open(freq_path, 'r').read().rstrip()

    
    if args.stats:
        stats(get_freq(file), freq, file[:args.length])
    if args.modulo:
        modulo(file[:args.length])


if __name__ == "__main__":
    main()
