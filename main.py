"""
    Cipher cracker
"""
import sys
import os
import re
import time # .sleep(), .time(), .time_ns()
import argparse
import numpy as np

"""
    Ideas:
    - Statistical analysis
"""

ALPHA = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#'
ALPHAS = [ALPHA, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_#0123456789', '_#0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ']

parser = argparse.ArgumentParser(
                    prog = 'crack',
                    description = 'Crack the ciphers of ACry course',
                    epilog = 'Cracking the cipher.')
parser.add_argument('path', help='the cipher to crack')      # option that takes a value

parser.add_argument('-v', '--verbose', help='verbosity', action='store_true')
parser.add_argument('-s', '--seq', help='count sequence of n chars', type=int, default=0)
parser.add_argument('-f', '--freq', nargs='?', default='freq.data',  help='frequency table', type=str)  # on/off flag
parser.add_argument('--digram', nargs='?', default='digram.data',  help='digram frequency table', type=str)  # on/off flag
parser.add_argument('-l', '--length', help='demo text length', default=100, type=int)
args = parser.parse_args()

def stats(text: str) -> None:
    """
        Statistical approach
    """
    freqtxt = get_freq(text)
    freq = open(args.freq, 'r').read().rstrip()
    digram = open(args.digram, 'r').read().rstrip().split('\n')
    if type(freq) is not list:
        freq = list(freq)
    for i in range(0, len(freqtxt)):
        if freqtxt[i] not in freq:
            freq.append(freqtxt[i])
        else:
            print(freqtxt[i] + ' -> ' + (freq[i] if freq[i] != '\n' else '~'))

    new = []
    for c in text[:args.length]:
        new.append(freq[freqtxt.index(c)])

    print(''.join(new))


def counter(d, k):
    if k not in d:
        d[k] = 1
    else:
        d[k] += 1

def get_freq(text):
    """
        Get characters in a list ordered by frequency
    """
    chars = {}
    for i in range(0, len(text)):
        if i-args.seq+1 >= 0:
            counter(chars, text[i-args.seq+1:i+1])
        else:
            continue
    ls = []
    for c in chars:
        ls.append([c, chars[c]])
    ls = sorted(ls, key=lambda x : x[1], reverse=True)
    if args.verbose:
        for x in ls:
            print(x[0] + ': ' + str(x[1]))
    ls = [x[0] for x in ls]

    return ls

def main():
    text = ''.join(open(args.path, 'r').read().rstrip().split('\n'))
    stats(text)

if __name__ == "__main__":
    main()
