"""
    Cipher cracker
"""
import sys
import os
import re
import time # .sleep(), .time(), .time_ns()
import argparse
import numpy as np

alpha = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#'
parser = argparse.ArgumentParser(prog = 'crack', description = 'Crack the ciphers of ACry course', epilog = 'Cracking the cipher.')
parser.add_argument('path', help='the cipher to crack')      # option that takes a value
parser.add_argument('-v', '--verbose', help='verbosity', action='store_true')
parser.add_argument('-s', '--seq', help='count sequence of n chars', type=int, default=0)
parser.add_argument('-f', '--freq', nargs='?', const=2, default=0,  help='frequency table', type=int) 
parser.add_argument('--bigram', nargs='?', default='bigram.data',  help='bigram frequency table', type=str)
parser.add_argument('-l', '--length', help='demo text length', default=100, type=int)
args = parser.parse_args()

frequency = " ETAOINSHRDLCUMWFGYPBVKJXQZ\n"
bigram = ['TH','HE','IN','ER','AN','RE','ON','AT','EN','ND','TI','ES','OR','TE','OF','ED','IS','IT','AL','AR','ST','TO','NT','NG','SE','HA','AS','OU','IO','HE','LE','IN','VE','ER','CO','AN','ME','RE','DE','ON','HI','AT','RI','EN','RO','ND','IC','TI','NE','ES','EA','OR','RA','TE','CE']
trigram = ['THE']

def counter(d, k):
    if k not in d:
        d[k] = 1
    else:
        d[k] += 1

def get_freq(text, seq=1, min_freq=0.00, exclude=''):
    """
        Get characters in a list ordered by frequency
    """
    chars = {}
    for i in range(0, len(text)):
        if i-seq+1 >= 0:
            t = text[i-seq+1:i+1]
            if (exclude and exclude not in t) or not exclude:
                counter(chars, t)
    ls = []
    for c in chars:
        ls.append([c, chars[c]])
    ls = sorted(ls, key=lambda x : x[1], reverse=True)
    if min_freq > 0:
        ls = filter(lambda x : (float(x[1]) / len(text)) >= min_freq, ls)
    if args.verbose:
        for x in ls:
            print(x[0] + ': ' + str(x[1]))
    ls = [x[0] for x in ls]

    return ls

def stats(text: str) -> None:
    """
        Statistical approach
    """
    fqs = get_freq(text)
    # Try to exclude one of the tops which should be space
    for c in fqs:
        bis = get_freq(text, seq=2, min_freq=0.02, exclude=c)
        print(bis)
        tris = get_freq(text, seq=3, min_freq=0.015, exclude=c)
        print(tris)


def main():
    text = ''.join(open(args.path, 'r').read().rstrip().split('\n'))
    stats(text)

if __name__ == "__main__":
    main()
